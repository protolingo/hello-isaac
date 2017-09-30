import json


LABELS_FILE = 'symbols/labels.json'


class LabelManager:

    def __init__(self):
        with open(LABELS_FILE) as f:
            self.labels = json.load(f)

    def __getitem__(self, default_label):
        return self.labels.get(default_label, default_label)

    def __setitem__(self, default_label, label):
        self.labels[default_label] = label
        with open(LABELS_FILE, 'w') as f:
            json.dump(self.labels, f, indent=4)


labels = LabelManager()
