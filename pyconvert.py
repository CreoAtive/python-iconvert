# python
import os
import sys
import subprocess

def convertFile(path = ''):
    '''convert file to .rat'''

    if os.path.isfile(path):
        root, extension = os.path.splitext(path)

        output_path = path.replace(extension, '.rat')

        cmd = ['iconvert', path, output_path, 'compression=rle']

        popen = subprocess.Popen(cmd, stdout = subprocess.PIPE)

        return popen

    raise Exception('Path is no file')

def scanDir(path = '', allowed_extensions = []):
    '''scan directory for files'''

    files = []

    if os.path.isdir(path):
        for file_name in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
            root, extension = os.path.splitext(file_name)

            if extension in allowed_extensions:
                files.append(os.path.normpath(os.path.join(path, file_name)))

        return files

    raise Exception('Path is no directory')

def displayProgress(current = 0, total = 0):
    os.system('cls')

    progress = (100.0 / total) * current
    progress_bar_total_length = 32
    progress_bar_length = int(progress_bar_total_length / 100.0 * progress)

    print 'Converting {current} of {total} files'.format(current = current, total = total)
    print '\r[{0}{1}] {2}%'.format('#'*progress_bar_length, '_'*(progress_bar_total_length - progress_bar_length), int(progress))

def convertFiles(files = [], batch_size = 1):
    threads = []

    for index, file_path in enumerate(files):
        displayProgress(index + 1, len(files))

        try:
            threads.append(convertFile(file_path))
        except Exception as e:
            pass

        if index % batch_size == 0:
            for thread in threads:
                thread.wait()

            threads = []

def prepArgs(*args):
    prepped_args = []
    prepped_kwargs = {}

    for arg in args:
        if '=' in arg:
            kwarg, kwarg_value = arg.split('=', 2)

            if kwarg:
                prepped_kwargs[kwarg] = kwarg_value
        else:
            prepped_args.append(arg)

    return prepped_args, prepped_kwargs

def main(*args, **kwargs):
    args, kwargs = prepArgs(*args)

    path = args[0]
    batch_size = 8

    if '--batch-size' in kwargs:
        try:
            arg_batch_size = int(kwargs['--batch-size'])
        except:
            pass
        else:
            batch_size = arg_batch_size

    try:
        convertFiles(scanDir(path, ['.exr', '.tiff', '.jpg', '.jpeg', 'png', '.hdr']), batch_size)
    except Exception as e:
        print e.message

if __name__ == '__main__':
    main(*sys.argv[1:])
