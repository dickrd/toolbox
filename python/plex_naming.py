#!/bin/env python
import os
import re


class TvShow(object):
    def __init__(self, name, save_location=None, create_link=False,
                 include_subtitle=False, subtitle_language="eng"):
        self.desired = name + " - S{0}E{1}{2}"
        self.save_location = save_location
        self.create_link = create_link
        self.include_subtitle = include_subtitle

        self.show_pattern = re.compile(r".*[sS]?(\d\d)[eEx](\d\d).*(\.(mkv|mp4|idx|sub|ass|srt))")
        if self.include_subtitle:
            self.desired_subtitle = name + " - S{0}E{1}." + subtitle_language + "{2}"


    def add(self, path, file_name):

        # Move to save directory.
        if self.save_location:
            output_directory = self.save_location
        # Or else, just rename in its original directory.
        else:
            output_directory = path

        original_file = os.path.join(path, file_name)
        r = self.show_pattern.match(file_name)

        # Not match regex.
        if not r:
            return

        # If the file is a subtitle file.
        if file_name.endswith(".ass") or file_name.endswith(".srt"):

            # Skip if not including subtitle.
            if not self.include_subtitle:
                return

            print("Processing subtitle: " + file_name)
            result_file = os.path.join(output_directory, self.desired_subtitle.format(r.group(1), r.group(2), r.group(3)))

        # Not a subtitle file.
        else:
            print("Processing video: " + file_name)
            result_file = os.path.join(output_directory, self.desired.format(r.group(1), r.group(2), r.group(3)))

        os.rename(original_file, result_file)
        if self.create_link:
            print("Creating symbolic link to: " + result_file)
            os.symlink(result_file, original_file)


def clean_video(directory, audio_languages=None):
    if audio_languages is None:
        audio_languages = ["eng"]

    from subprocess import call
    for path, directories, files in os.walk(directory):
        print("In: " + path)
        for file_name in files:
            if file_name.endswith(".mkv"):
                print("Processing using mkvproedit: " + file_name)
                call(["mkvpropedit", os.path.join(path, file_name), "--quiet", "-d", "title"])
                call(["mkvpropedit", os.path.join(path, file_name), "--quiet", "-e", "track:v1", "-d", "name"])

                for index, item in enumerate(audio_languages, 1):
                    call(["mkvpropedit", os.path.join(path, file_name), "--quiet", "-e",
                          "track:a{0}".format(index), "-d", "name"])
                    call(["mkvpropedit", os.path.join(path, file_name), "--quiet", "-e",
                          "track:a{0}".format(index), "-s", "language={0}".format(item)])

            elif file_name.endswith(".mp4") or file_name.endswith(".avi"):
                print("Processing using ffmpeg: " + file_name)
                tmp_name = "ptuil_tmp_ffmpeg.mp4"
                process = ["ffmpeg", "-i", os.path.join(path, file_name), "-codec", "copy", "-hide_banner", "-loglevel", "panic",
                 "-map_metadata", "-1"]

                for index, item in enumerate(audio_languages, 0):
                    process.append("-metadata:s:a:{0}".format(index))
                    process.append("language={0}".format(item))
                process.append(tmp_name)
                call(process)

                if file_name.endswith(".mp4"):
                    os.rename(tmp_name, os.path.join(path, file_name))
                else:
                    os.rename(tmp_name, os.path.join(path, file_name[:-4] + ".mp4"))
                    os.remove(os.path.join(path, file_name))
            else:
                print("Skip file: " + file_name)


def split_video(video_path, time, name):
    from subprocess import call
    print("Splitting video at {0}, to {1} and {2}".format(time, name[0], name[1]))
    call(["ffmpeg", "-i", video_path, "-hide_banner", "-loglevel", "panic",
          "-t", time, "-c", "copy", name[0],
          "-ss", time, "-c", "copy", name[1]])


def _util():
    import argparse

    # Parse commandline arguments.
    parser = argparse.ArgumentParser(description="util for plex videos.")
    parser.add_argument("action",
                        help="action to perform, including: rename, clean, split")
    parser.add_argument("-i", "--input-path", default="./",
                        help="path to video and subtitle files")
    parser.add_argument("-n", "--show-name",
                        help="show name of video files")
    parser.add_argument("-o", "--save-location", default=None,
                        help="save result to this directory")

    parser.add_argument("--create-link", action="store_true",
                        help="if leave a symbolic link in the original place")
    parser.add_argument("--include-subtitle", action="store_true",
                        help="if include subtitle when rename")
    parser.add_argument("--language", default=None, nargs="+",
                        help="set language")
    parser.add_argument("--time",
                        help="time code to split")
    parser.add_argument("--result-names", default=None, nargs="2",
                        help="set split file names")

    args = parser.parse_args()

    if args.action == "rename":
        if not args.show_name:
            print("Name of the show is required (--show-name).")
            return

        if args.save_location:
            if not os.path.isdir(args.save_location):
                print("Invalid save location.")
                return
            print("Result file will be saved to: " + args.save_location)
        else:
            print("Result file will be saved to its original directory.")

        if args.create_link:
            print("Original file structure will remain the same.")

        subtitle_language = "eng"
        if args.include_subtitle:
            print("Subtitle will be renamed.")
            if args.language:
                subtitle_language = args.language[0]
            print("Set subtitle language to: " + subtitle_language)

        a_show = TvShow(name=args.show_name, save_location=args.save_location,
                        create_link=args.create_link, include_subtitle=args.include_subtitle, subtitle_language=subtitle_language)

        for path, directories, files in os.walk(args.input_path):
            print("In \"{0}\"".format(path))
            for file_name in files:
                a_show.add(path, file_name)

    elif args.action == "clean":
        if args.language:
            print("Set audio languages to: {0}".format(args.language))

        clean_video(args.input_path, args.language)

    elif args.action == "split":
        if not args.time:
            print("Split time code is required (--time).")
            return
        if not args.result_names:
            print("Name of the result file is required (--result-names).")
            return

        split_video(args.input_path, args.time, args.result_names)

    else:
        print("Unsupported action: " + args.action)


if __name__ == '__main__':
    _util()
