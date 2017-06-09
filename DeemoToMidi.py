import json, os, midiutil, argparse

def convert_file(json_path, dest):
    with open(json_path) as f:
        data = json.load(f)
    mid = midiutil.MIDIFile(1)
    for notes in data['notes']:
        if 'sounds' not in notes:
            continue
        if '_time' not in notes:
            time = 0
        else:
            time = notes['_time']
        for note in notes['sounds']:
            if 'd' not in note:
                continue
            if note['d']==0 or note['v']==0:
                continue
            mid.addNote(0,0,note['p'],time,note['d'],note['v'])
    with open(dest, 'wb') as output_file:
        mid.writeFile(output_file)

def convert_dir(input_folder, dest_folder):
    file_names=[fn for fn in os.listdir(input_folder) if fn[-13:]=='hard.json.txt']
    for json_file in file_names:
        convert_file(os.path.join(input_folder,json_file), os.path.join(dest_folder,json_file+'.mid'))
        try:
            convert_file(os.path.join(input_folder,json_file), os.path.join(dest_folder,json_file+'.mid'))
        except:
            print(json_file, ' is not converted.')

if __name__ == '__main__':
    location = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(description='Deemo json to midi converter.')
    parser.add_argument('-i', '--input', type=str, default=location, help='input folder location')
    parser.add_argument('-d', '--destination', type=str, default=location, help='output folder location')
    args = parser.parse_args()
    convert_dir(args.input, args.destination)
