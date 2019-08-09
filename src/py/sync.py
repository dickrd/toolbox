import hashlib
import os

BUFFER_SIZE = 2048000


def sync(source, destination, states):
    src_directory, src_folders, src_files = next(os.walk(source))
    dst_directory, src_folders, dst_files = next(os.walk(destination))
    for a_file in src_files:
        src_file_path = os.path.join(src_directory, a_file)
        dst_file_path = os.path.join(dst_directory, a_file)

        # if destination has file
        if a_file in dst_files:
            dst_file_hash = _buffered_hash(dst_file_path)

            # and states tracked file
            if src_file_path in states:
                # and hash matches
                if states[src_file_path] == dst_file_hash:
                    # all good
                    continue
                # and hash mismatch
                else:
                    _notify_user("hash mismatch: {}, {}".format(states[src_file_path], dst_file_hash))
                    continue

            # and not tracked by states
            src_file_hash = _buffered_hash(src_file_path)

            # add track record if they match hash
            if src_file_hash == dst_file_hash:
                states[src_file_path] = src_file_hash
                continue

            _notify_user("hash mismatch: {}, {}".format(src_file_hash, dst_file_hash))


def _buffered_hash(file_path):
    md5 = hashlib.md5()
    with open(file_path, "rb") as file_stream:
        buffer = file_stream.read(BUFFER_SIZE)
        while buffer:
            md5.update(buffer)
            buffer = file_stream.read(BUFFER_SIZE)
    return md5.hexdigest()

# TODO: email
def _notify_user(message):
    print(message)
