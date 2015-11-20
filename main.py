import sys

from mass_dtw import MassDtw


def interpret_run(cmd):
    if any(x in cmd for x in ['help', '-help', '--help', '-h', '-H']):
        print()
        print("Usage:")
        print("\tpython {} [flags]"
              .format(cmd[0]))
        print()
        print("Flags: (and it's default values)")
        print("   -label=rotulos.txt - File with labels to the \
classes of series.")
        print("   -base=treino.txt   - File with the base temporal series.")
        print("   -compare=teste.txt - File to check the temporal series.")
        print("   -sc_band=100       - Percentage of the Sakoe-Chiba band \
(integer values between 0 and 100).")
        print()
        print("Please, avoid spaces on the filenames.")
        print()

        sys.exit()

    flags = {'compare': "teste.txt",
             'base': "treino.txt",
             'label': "rotulos.txt",
             'sc_band': "100"}

    for flag in cmd[1:]:    # Interpret all flags
        try:
            flagname, flagcontent = flag[1:].split('=', 1)
            if flagname in flags:
                flags[flagname] = flagcontent
            else:
                raise Exception
        except Exception:
            print('Ignoring flag: {}'.format(flag))

    # Check if 'sc_band' can be converted to a number,
    # to avoid further Try/Catch
    if not flags['sc_band'].isdigit():
        print('Ignoring flag: -sc_band={}'.format(flags['sc_band']))
        flags['sc_band'] = "100"

    return flags

# ----- Script starts here:
import os
os.system('sudo echo ""')
flags = interpret_run(sys.argv)

# Open Files
try:
    file_compare = open(flags['compare']).read()
    file_base = open(flags['base']).read()
    file_label = open(flags['label']).read()
except IOError as e:
    print("Can't open one of the files.")
    raise e

mass_dtw = MassDtw(file_base,
                   file_compare,
                   file_label=file_label,
                   sc_band=flags['sc_band'])

ratio = mass_dtw.run()
print('{}%'.format(ratio))
print(mass_dtw.get_time_last_run)
os.system('sudo beep')
