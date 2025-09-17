
import re
import copy

def extract_event_line(line):
    match = re.search(r"EVENTID:\s*\d+\s+([A-Z0-9_]+)", line)
    if match:
        return match.group(1)
    else:
        return False

def extract_type_line(line):
    match = re.search(r'Type:\s*([^\s,]+)', line)
    if match:
        return match.group(1)
    else:
        return False

def extract_msf_line(line):
    msf_pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2})$')
    msf_triplets = None

    match = msf_pattern.search(line)
    if match:
        msf_triplets = ([int(match.group(1)), int(match.group(2)), int(match.group(3))])
        offset2352 = ((msf_triplets[0] * 60 * 75) + ((msf_triplets[1] - 2) * 75) + (msf_triplets[2] * 1)) * 2352;
        offset = ((msf_triplets[0] * 60 * 75) + ((msf_triplets[1] - 2) * 75) + (msf_triplets[2] * 1));
        return offset
    return False

ext_map = {
    "mapmdl": "mmd",
    "maptex": "mtd",
}

def filter_lines(input_lines):
    keywords = ["CdlSetloc", "LoadAsset", "EVENTID"]
    new_list = []
    for line in input_lines:
        if any(keyword in line for keyword in keywords):
            new_list.append(line.rstrip())
    return new_list

class loadentry:
    def __init__(self):
        self.sector_offset = None
        self.file_type     = None
        self.event_line    = None
        self.folder        = None

def extract_log_data():
    with open("loaddata.txt", "r") as inData:
        lines = inData.readlines()
        lines = filter_lines(lines)
        entries = []
        final_entries = []
        g_last_event = None
        for idx, lin in enumerate(lines):

            #print(lin)
            entry = loadentry()
            entry.sector_offset = extract_msf_line(lin)
            entry.file_type    = extract_type_line(lin)
            entry.event_line   = extract_event_line(lin)

            if entry.event_line:
                g_last_event = entry.event_line

            entry.folder = g_last_event

            if entry.file_type in ext_map.keys():
                entry.file_type = ext_map[entry.file_type]

            entries.append(entry)

        for idx, entry in enumerate(entries):
            entry = copy.deepcopy(entries[idx])
            if entries[idx].sector_offset:
                if entries[idx - 1].file_type:
                    entry.file_type = f".{entries[idx - 1].file_type}"
            final_entries.append(entry)

    #return entries
    return final_entries

if __name__ == "__main__":
    entries = extract_log_data()

    for idx, entry in enumerate(entries):
        if entry.sector_offset:
            if entry.file_type:
                print(f"{entry.folder} {entry.sector_offset} {entry.file_type}")
            else:
                print(f"{entry.folder} {entry.sector_offset}")
    