#!/usr/bin/env python3

import os
import time
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import convert_to_html

class MarkdownFileHandler(FileSystemEventHandler):
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

        print('Watching file: {}'.format(self.input_file))
        print("Startup conversion...")
        convert_to_html.main(self.input_file, self.output_file)

    def on_modified(self, event):
        if event.src_path.endswith(self.input_file):
            convert_to_html.main(self.input_file, self.output_file)
            print('File modified: {}'.format(self.input_file))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='input Markdown file')

    # default output file is input file with .html extension
    parser.add_argument('output_file', help='output HTML file', nargs='?', default=None)
    args = parser.parse_args()

    if args.output_file is None:
        args.output_file = os.path.splitext(args.input_file)[0] + '.html'

    if not os.path.exists(args.input_file):
        # create the file if it doesn't exist
        open(args.input_file, 'a').close()

    event_handler = MarkdownFileHandler(args.input_file, args.output_file)

    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(args.input_file) or '.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    main()