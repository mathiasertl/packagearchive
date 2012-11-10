import gnupg

class Package(dict):
    def __init__(self, path):
        self.path = path

    def parse(self):
        self.data = gnupg.GPG().decrypt_file(open(self.path, 'rb'))
        if not self.data.valid:
            raise RuntimeError("%s: GPG signature not valid" % self.path)

        last_field = None
        for line in self.data.data.strip().split("\n"):
            if line.startswith(' '):
                # append to last line
                if self[last_field] == '':
                    self[last_field] = line[1:]
                else:
                    self[last_field] += "\n%s" % line[1:]
            else:
                field, value = line.split(':', 1)
                field = field.strip()
                value = value.strip()

                last_field = field
                self[field] = value

    def get_files(self):
        if 'Files' in self:
            raw = self.get('Files')
        else:
            raw = self.get([k for k in self.keys() if k.startswith('Checksums')][0])

        files = []
        for line in raw.split("\n"):
            files.append(line.split()[-1])

        return files

class SourcePackage(Package):
    pass


class BinaryPackage(Package):
    pass
