import subprocess
import sys

import yaml


def generate_rules_function(_rules):
    _str = []
    rule_function_name = None
    space = ' '
    valid_types = ['single', 'array']

    try:
        for rule in _rules:
            rule_function_name = rule['name'].strip()
            rule_type = rule['type'].strip()
            extract = rule['extract']
            what = extract['what']

            if 'name' in extract:
                name = extract['name']

            if rule_type not in valid_types:
                print('Incorrect type. Valid types are: array, single')
                not_found = True
                break

            css_selector = rule['selector'].strip()
            rule_function_name = '{}'.format(rule_function_name)

            _str.append('def get_{}(soup_object):'.format(rule_function_name))
            if rule_type.lower() == 'array'.lower():
                _str.append('\t_{} = []'.format(rule['name'].strip()))
            else:
                _str.append('\t_{} = None'.format(rule['name'].strip()))

            _str.append('\t{}_section = soup_object.select("{}")\n'.format(rule_function_name, css_selector))
            _str.append('\tif len({}_section) > 0:'.format(rule_function_name))

            if rule_type.lower() == 'array'.lower():
                _str.append('\t\tfor item in {}_section:'.format(rule_function_name).ljust(14, ' '))
            else:
                _str.append('\t\t_{} = {}_section[0].text.strip()'.format(rule_function_name, rule_function_name))

            if what == 'attribute' and name == 'href':
                _str.append("\t\t\turl = item['href'] ")
                _str.append("\t\t\t_{}.append({})".format(rule['name'].strip(), 'url'))

            _str.append('\treturn _{}'.format(rule['name'].strip()))
            _str.append('\n\n')
    except Exception as ex:
        print('Exception in generate_rules_function')
        print(str(ex))
    finally:
        return _str


def generate_func_body(_rules, func_name):
    _str = []

    try:
        _str.append('def {}({}): \n'.format(func_name, '_url'))
        _str.append('\tr = requests.get({})'.format('_url'))
        _str.append('\tif r.status_code == 200:')
        _str.append('\t\thtml = r.text.strip()')
        _str.append('\t\tsoup = BeautifulSoup(html,\'lxml\')')

        for rule in _rules:
            rule_function_name = rule['name'].strip()
            if 'get' not in rule_function_name:
                rule_function_name = '{} = get_{}'.format(rule_function_name, rule_function_name)
                _str.append('\t\t{}(soup)'.format(rule_function_name))
    except Exception as ex:
        print('Exception in generate_func_body')
        print(str(ex))
    finally:
        return _str


def generate_main(_main):
    _str = []
    try:
        _str.append("\n\nif __name__ == '__main__':")
        _str.append('   main_url = "{}"'.format(_main['entry_url']))
        _str.append('   {}({})'.format(_main['entry_function'], 'main_url'))
    except Exception as ex:
        print('Exception in Generate Main')
        print(str(ex))
    finally:
        return _str


if __name__ == '__main__':
    not_found = False
    script_name = None
    file_output = []
    yaml_file = None

    try:
        args = sys.argv
        if len(args) != 2:
            print('Err... the correct format is: python parse_gen.py <YAML file>')
            exit()

        yaml_file = args[1]
        required = ['script_name', 'lib', 'main', 'function_name', 'rules']
        y = yaml.load(open(yaml_file), Loader=yaml.FullLoader)

        for k in y:
            if k not in required:
                print('Halt! {} is not present. It is required'.format(k))
                not_found = True
                break

        if not not_found:
            script_name = y['script_name']
            main_section = y['main']
            rules_section = y['rules']

            rules_content = generate_rules_function(rules_section)
            main_content = generate_main(main_section)
            func_content = generate_func_body(rules_section, main_section['entry_function'])

            if not not_found:
                with open(script_name, 'w', encoding='utf8') as f:
                    f.write('import requests\n')
                    f.write('from bs4 import BeautifulSoup\n\n')
                    f.write('\n'.join(rules_content))
                    f.write('\n'.join(func_content))
                    f.write('\n'.join(main_content))

            print('Formatting the code file: {}. Please wait...'.format(script_name))
            subprocess.call('autopep8 -i {}'.format(script_name), shell=True)
    except Exception as ex:
        print('Main Exception')
        print(str(ex))
