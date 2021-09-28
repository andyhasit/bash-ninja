import sys, os
from collections import defaultdict

def extract(filepath):
    with open(filepath) as fp:
        for linenumber, line in enumerate(fp):
            try:
                processline(line)
            except Exception as e:
                print("problem at line {0}".format(linenumber))
                print(e)

def processline(line):
    line = line.strip()
    if line == '':
        return
    sections, command = splitline(line)
    create_alias(sections, command)
    all_sections.append(sections)

def create_alias(sections, command):
    s = create_alias_string(sections)
    if aliases.has_key(s):
        raise ValueError("Alias {0} already exists".format(s))
    aliases[s] = command

def create_alias_string(sections):
    return PREFIX + ''.join([s[0] for s in sections])

def splitline(line):
    end = line.index(':')
    sections = line[0: end].strip().split(' ')
    command = line[end + 1:].strip()
    return sections, command

def create_help_aliases(all_sections):
    help_aliases_entries = defaultdict(list)
    for sectionset in all_sections:
        entry = '  ' + sectionset[-1]
        parent = create_alias_string(sectionset[:-1])
        help_aliases_entries[parent].append(entry)
        #Add as menu if not exists
        if len(sectionset) > 1:
            parent = create_alias_string(sectionset[:-2])
            entry = '  *' + sectionset[-2]
            if entry not in help_aliases_entries[parent]:
                help_aliases_entries[parent].append(entry)
    help_aliases = {}
    for k in sorted(help_aliases_entries):
        help_aliases[k] = 'printf "available entries:\\n' + "\\n".join(help_aliases_entries[k]) + '\\n"'
    return help_aliases

def write_alias_lists_to_file(alias_file, *alias_dicts):
    total = 0
    with open(alias_file, 'w+') as fd:
        for alias_dict in alias_dicts:
            for k in alias_dict:
                fd.write("alias {0}='{1}'\n".format(k, alias_dict[k]))
                total += 1
    print("Wrote {0} aliases to file: {1}".format(total, alias_file))

aliases = {}
all_sections = []

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Call with PREFIX CONF_FILE ALIASES_FILE')
        exit(1)
    THIS_SCRIPT = os.path.realpath(__file__)
    PREFIX = sys.argv[1]
    CONF_FILE = os.path.realpath(sys.argv[2])
    ALIASES_FILE = os.path.realpath(sys.argv[3])
    print('CONF_FILE: ' + CONF_FILE)
    print('ALIASES_FILE: ' + ALIASES_FILE)
    aliases[PREFIX + 'edit'] = 'nano "{CONF_FILE}" && python "{THIS_SCRIPT}" \
"{PREFIX}" "{CONF_FILE}" "{ALIASES_FILE}" && source "{ALIASES_FILE}"'.format(
        ALIASES_FILE=ALIASES_FILE,
        CONF_FILE=CONF_FILE,
        THIS_SCRIPT=THIS_SCRIPT,
        PREFIX=PREFIX
        )
    extract(CONF_FILE)
    help_aliases = create_help_aliases(all_sections)
    write_alias_lists_to_file(ALIASES_FILE, aliases, help_aliases)

'''
python ninj.py nj '~/Documents/ninja_aliases.conf' '~./nj_aliases'

alias ninj="nano ~/Documents/ninja_aliases.conf && source ~/Documents/ninja_aliases.conf"
'''


