import sys
import argparse
import csv
import logging
import bisect
import math
import re
import string

# Initialized later
policy_list = {}
PASSWORD_END = '\n'


class BasePasswordPolicy(object):
    def pwd_complies(self, pwd):
        raise NotImplementedError()

    @staticmethod
    def fromConfig(config):
        return policy_list[config.enforced_policy]


class BasicPolicy(BasePasswordPolicy):
    def pwd_complies(self, pwd):
        return True


class PasswordPolicy(BasePasswordPolicy):
    def __init__(self, regexp):
        self.re = re.compile(regexp)

    def pwd_complies(self, pwd):
        return self.re.match(pwd) is not None


class ComplexPasswordPolicy(BasePasswordPolicy):
    digits = set(string.digits)
    uppercase = set(string.ascii_uppercase)
    lowercase = set(string.ascii_lowercase)
    upper_and_lowercase = set(string.ascii_uppercase + string.ascii_lowercase)
    non_symbols = set(
        string.digits + string.ascii_uppercase + string.ascii_lowercase)

    def __init__(self, required_length=8):
        self.blacklist = set()
        self.required_length = required_length

    def load_blacklist(self, fname):
        with open(fname, 'r') as blacklist:
            for line in blacklist:
                self.blacklist.add(line.strip('\n'))

    def has_group(self, pwd, group):
        return any(map(lambda c: c in group, pwd))

    def all_from_group(self, pwd, group):
        return all(map(lambda c: c in group, pwd))

    def passes_blacklist(self, pwd):
        return (''.join(filter(
            lambda c: c in self.upper_and_lowercase, pwd)).lower()
                not in self.blacklist)

    def pwd_complies(self, pwd):
        pwd = pwd.strip(PASSWORD_END)
        if len(pwd) < self.required_length:
            return False
        if not self.has_group(pwd, self.digits):
            return False
        if not self.has_group(pwd, self.uppercase):
            return False
        if not self.has_group(pwd, self.lowercase):
            return False
        if self.all_from_group(pwd, self.non_symbols):
            return False
        return self.passes_blacklist(pwd)


class ComplexPasswordPolicyLowercase(ComplexPasswordPolicy):
    def pwd_complies(self, pwd):
        pwd = pwd.strip(PASSWORD_END)
        if len(pwd) < self.required_length:
            return False
        if not self.has_group(pwd, self.digits):
            return False
        if not self.has_group(pwd, self.upper_and_lowercase):
            return False
        if self.all_from_group(pwd, self.non_symbols):
            return False
        return self.passes_blacklist(pwd)


class OneUppercasePolicy(ComplexPasswordPolicy):
    def pwd_complies(self, pwd):
        pwd = pwd.strip(PASSWORD_END)
        if len(pwd) < self.required_length:
            return False
        if not self.has_group(pwd, self.uppercase):
            return False
        return self.passes_blacklist(pwd)


class SemiComplexPolicyLowercase(ComplexPasswordPolicy):
    def pwd_complies(self, pwd):
        pwd = pwd.strip(PASSWORD_END)
        count = 0
        if len(pwd) < self.required_length:
            return False
        if self.has_group(pwd, self.digits):
            count += 1
        if self.has_group(pwd, self.upper_and_lowercase):
            count += 1
        if self.all_from_group(pwd, self.non_symbols):
            count += 1
        return self.passes_blacklist(pwd) and count >= 2


class SemiComplexPolicy(ComplexPasswordPolicy):
    def pwd_complies(self, pwd):
        pwd = pwd.strip(PASSWORD_END)
        count = 0
        if len(pwd) < self.required_length:
            return False
        if self.has_group(pwd, self.digits):
            count += 1
        if self.has_group(pwd, self.uppercase):
            count += 1
        if self.has_group(pwd, self.lowercase):
            count += 1
        if self.all_from_group(pwd, self.non_symbols):
            count += 1
        return self.passes_blacklist(pwd) and count >= 3


policy_list = {
    'complex': ComplexPasswordPolicy(),
    'basic': BasicPolicy(),
    '1class8': PasswordPolicy('.{8,}'),
    'basic_long': PasswordPolicy('.{16,}'),
    'complex_lowercase': ComplexPasswordPolicyLowercase(),
    'complex_long': ComplexPasswordPolicy(16),
    'complex_long_lowercase': ComplexPasswordPolicyLowercase(16),
    'semi_complex': SemiComplexPolicy(12),
    'semi_complex_lowercase': SemiComplexPolicyLowercase(12),
    '3class12': SemiComplexPolicy(12),
    '2class12_all_lowercase': SemiComplexPolicyLowercase(12),
    'one_uppercase': OneUppercasePolicy(3)
}


class GuessSerializer(object):
    TOTAL_COUNT_RE = re.compile('Total count: (\d*)\n')
    TOTAL_COUNT_FORMAT = 'Total count: %s\n'

    def __init__(self, ostream):
        self.ostream = ostream
        self.total_guessed = 0

    def serialize(self, password, prob):
        if prob == 0:
            return
        if type(password) == tuple:
            password = ''.join(password)
        self.total_guessed += 1
        self.ostream.write('%s\t%s\n' % (password, prob))

    def get_total_guessed(self):
        return self.total_guessed

    def collect_answer(self, real_output, istream):
        for line in istream:
            real_output.write(line)

    def finish_collecting(self, real_output):
        logging.info('Finishing aggregating child output')
        real_output.flush()

    def get_stats(self):
        raise NotImplementedError()

    def finish(self):
        self.ostream.flush()
        self.ostream.close()


class DelAmicoCalculator(GuessSerializer):
    def __init__(self, ostream, pwd_list, random_walk_confidence_bound_z_value=1.96):
        super().__init__(ostream)
        self.pwds, self.probs = zip(*sorted(pwd_list, key=lambda x: x[1]))
        self.pwds = list(self.pwds)
        for i, pwd in enumerate(self.pwds):
            if type(pwd) == tuple:
                self.pwds[i] = ''.join(pwd)
        self.guess_numbers = []
        for _ in range(len(self.pwds)):
            self.guess_numbers.append([])
        self.random_walk_confidence_bound_z_value = random_walk_confidence_bound_z_value

    def serialize(self, pwd, prob):
        self.total_guessed += 1
        if prob == 0:
            return
        idx = bisect.bisect_left(self.probs, prob) - 1
        if idx >= 0:
            self.guess_numbers[idx].append(prob)

    def get_stats(self):
        out_guess_numbers = [0] * len(self.guess_numbers)
        out_variance = [0] * len(self.guess_numbers)
        out_stdev = [0] * len(self.guess_numbers)
        out_error = [0] * len(self.guess_numbers)
        num_guess = self.get_total_guessed()
        guess_nums = list(map(lambda items: list(
            map(lambda x: 1 / x, items)), self.guess_numbers))
        for i in range(len(self.guess_numbers)):
            out_guess_numbers[i] = sum(guess_nums[i]) / num_guess
        for j in range(len(out_guess_numbers) - 1, 0, -1):
            out_guess_numbers[j - 1] += out_guess_numbers[j]
        for i in range(len(self.guess_numbers)):
            out_variance[i] = (sum(map(
                lambda e: (e - out_guess_numbers[i]) ** 2, guess_nums[i])) /
                               num_guess)
        for j in range(len(out_guess_numbers) - 1, 0, -1):
            out_variance[j - 1] += out_variance[j]
        out_stdev = list(map(math.sqrt, out_variance))
        for i in range(len(self.guess_numbers)):
            out_error[i] = self.random_walk_confidence_bound_z_value * (
                out_stdev[i] / math.sqrt(num_guess))
        for i in range(len(self.pwds), 0, -1):
            idx = i - 1
            yield [
                self.pwds[idx], self.probs[idx], out_guess_numbers[idx],
                out_stdev[idx], num_guess, out_error[idx]]

    def finish(self):
        logging.info('Guessed %s passwords', self.get_total_guessed())
        writer = csv.writer(self.ostream, delimiter='\t', quotechar=None)
        for item in self.get_stats():
            writer.writerow(item)
        self.ostream.flush()
        self.ostream.close()


def main(args):
    input_probs = []
    prob_fmt = float.fromhex if args.hex else float
    policy = policy_list[args.policy]
    for pwd, prob in csv.reader(args.testfile, delimiter='\t', quotechar=None):
        prob_v = prob_fmt(prob)
        if 0 <= prob_v < 1:
            input_probs.append((pwd, prob_v))
    calculator = DelAmicoCalculator(
        args.ofile, input_probs, random_walk_confidence_bound_z_value=args.confidence_interval)
    filtered_policy_num, filtered_not_prob_num, ctr = 0, 0, 0
    batch_size = 1000000
    for row in csv.reader(args.randomfile, delimiter='\t', quotechar=None):
        if not args.flip_random_input_columns:
            pwd, prob_str = row
        else:
            prob_str, pwd = row
        prob = prob_fmt(prob_str)
        ctr += 1
        if ctr % batch_size == 0:
            print("Batch %d/%d" % (ctr/batch_size, batch_size))
        if not policy.pwd_complies(pwd):
            calculator.serialize(pwd, 0)
            filtered_policy_num += 1
        elif prob >= 0:
            calculator.serialize(pwd, prob)
        elif prob >= 1:
            calculator.serialize(pwd, 0)
            filtered_not_prob_num += 1
    calculator.finish()
    sys.stderr.write('Analyzed %d randomly generated passwords\n' % ctr)
    sys.stderr.write(('Filtered %d passwords for not satisfying '
                      'the %s policy\n') % (filtered_policy_num, args.policy))
    sys.stderr.write('Filtered %d passwords for out of bounds probability\n' %
                     filtered_not_prob_num)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=('Takes randomly generated passwords as input, and test'
                     ' password probabilities and calculates guess numbers. '))
    parser.add_argument('-randomfile', type=argparse.FileType('r'),
                        default=open(r'D:\data\leak_final_20161219\pipw_1.0\bpe2char_random_result.txt', 'r'),
                        help=('Randomly generated passwords file. Should be a '
                              'tsv where the first column is probability and '
                              'second column is the password. '))
    parser.add_argument('-testfile', type=argparse.FileType('r'),
                        default=open(r'D:\data\leak_final_20161219\pipw_1.0\bpe2char_test_result.txt', 'r'),
                        help=('Password file. Should be a tsv of passwords '
                              'where the first column is the probability and '
                              'second is the password. '))
    parser.add_argument('-o', '--ofile', type=argparse.FileType('w'),
                        default=open(r'D:\data\leak_final_20161219\pipw_1.0\bpe2char_guess_number.txt',
                                     'w',
                                     newline=''),
                        help='Output file. Default is stdout. ')
    """
    parser.add_argument('-o', '--ofile', type=argparse.FileType('w'),
                        default=open(r'D:\data\leak_final_20161219\pcfg\pcfg_guess_number.txt', 'w'),
                        help='Output file. Default is stdout. ')
    """
    parser.add_argument('-c', '--confidence-interval', type=float, default=1.96,
                        help=('Float of the confidence bound. Should be a '
                              'lookup in the theta table. Default is 1.96 '
                              'which corresponds to a 95 percent confidence '
                              'interval. '))
    parser.add_argument('--hex', action='store_true',
                        help='Probabilities are in hex format. ')
    parser.add_argument('-p', '--policy', default='basic',
                        choices=sorted(policy_list.keys()),
                        help='Password policy. Default is no policy. ')
    parser.add_argument('-f', '--flip-random-input-columns',
                        action='store_true')
    main(parser.parse_args())
