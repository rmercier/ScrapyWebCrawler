def find_between(s, first, last):
    try:
        start = s.index(first) + len(first);
        end = s.rindex(last, start);
        return s[start:end];
    except ValueError:
        return "";

def parseTransport(HTML):
    transportMode = dict();

    for line in HTML:
        key = find_between(line, 'class="', '"');
        content = find_between(line, '</i>', '</li>');
        #content = find_between(line, '</i>', '</li>').split(', ');
        transportMode[key] = content;

    return transportMode;
