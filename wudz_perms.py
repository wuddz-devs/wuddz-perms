import argparse, re, sys, string
from os import system
from itertools import product, permutations
system('')


def all_uplow_perms(pw):
    for w in map(''.join, product(*zip(pw.upper(), pw.lower()))):
        yield str(w)

def all_norep_perms(pw):
    for w in map(''.join, permutations(pw, len(pw))):
        yield str(w)

def all_perms(pw,pl):
    for w in map(''.join, product(pw, repeat=int(pl))):
        yield str(w)

def all_mac_perms(pre,suf,ml):
    for m in map(''.join, product("ABCDEF1234567890", repeat=int(ml))):
        yield str((':'.join(re.findall('.{1,2}', pre+m+suf))).upper())

def mac_data(m):
    if ':' in m:m = ''.join(str(m).split(':'))
    return m, 12-len(m)

def mac_setup(pre,suf):
    for i in ['pre','suf']:
        try:
            ms, ml = mac_data(eval(i))
            if ms and ml < 12:return ms,ml,i
        except:pass

def main(args):
    md = ''
    with open(args.output, 'a', encoding='utf-8') as fw:
        mc = {'pre':args.prefix,'suf':args.suffix}
        try:
            if args.all:
                if args.length is None:args.length = len(args.string)
                if args.string is None:args.string = (string.ascii_letters+string.digits+string.punctuation).strip()
                if args.string and args.length:md = all_perms(args.string,args.length)
            elif args.mac:
                ms, ml, mi = mac_setup(args.prefix,args.suffix)
                mc[str(mi)] = ms
                md = all_mac_perms(mc['pre'],mc['suf'],ml)
                mc = {'pre':'','suf':''}
            elif args.uplow:md = all_uplow_perms(args.string)
            elif args.norep:md = all_norep_perms(args.string)
        except:pass
        if md:
            c = 0
            print("\033[1;37;40m[*] Generating Combinations...\033[0m")
            while True:
                try:
                    fw.write('{}{}{}\n'.format(mc['pre'],next(md),mc['suf']))
                    c += 1
                except:break
            print("\033[1;32;40m[+] Saved {} Combinations To {}\033[0m".format(c,args.output))
        else:print("\033[1;31;40m[-] Error Occurred\033[0m")

def cli_main():
    parser = argparse.ArgumentParser(add_help = True, 
             description="Generate All/Non-Repeat Character Permutations/Combinations Of String Or Mac Addresses With Prefix/Suffix Partial Address.")
    parser.add_argument('-a', '--string', type=str, default=None, help='String To Generate All Permutations/Combinations.')
    parser.add_argument('-p', '--prefix', type=str, default='', help='String To Prefix Each Generated Permutation With.')
    parser.add_argument('-s', '--suffix', type=str, default='', help='String To Suffix Each Generated Permutation With.')
    parser.add_argument('-o', '--output', type=str, default='perms_output.txt', help='Output File To Save Generated Permutations To.')
    parser.add_argument('-l', '--length', type=int, default=None, help='Integer Length Of Characters To Be Generated.')
    parser.add_argument('-all', '--all', action='store_true', help='Generate All Combinations Of String.')
    parser.add_argument('-upl', '--uplow', action='store_true', help='Generate All Lower & Upper Case Permutations Of String.')
    parser.add_argument('-nrc', '--norep', action='store_true', help='Generate All Non Repeat Character Permutations Of String.')
    parser.add_argument('-mac', '--mac', action='store_true', help='Generate Mac Addresses With Specified Prefix/Suffix.')
    if len(sys.argv)==1:parser.print_help()
    else:main(parser.parse_args())
