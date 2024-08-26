import sys
import csv

# Create dictionaries to store the tag match counts and port/protocol match counts.
# These will eventually be used to create the output.
tag_matches = {} # Key: 'tag', Value: count
port_protocol_matches = {} # Key: ('dstport', 'protocol'), Value: count

# Create dict to store the number/keyword mappings from the IANA protocol number CSV
# found in the project directory.
# IANA CSV obtained here: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
protocol_lookup = {} # Key: Decimal, Value: Keyword
with open('protocol-numbers-1.csv', 'r', newline='') as iana_csv:
    reader = csv.DictReader(iana_csv)
    for row in reader:
        protocol_lookup.update({row['Decimal']: (str)(row['Keyword']).lower()})
iana_csv.close()

# Create dict to store the port/protocol to tag mappings from the provided lookup table.
# The filename for the lookup table CSV is given by the second command line argument
# after main.py.
tag_lookup = {} # Key: ('dstport', 'protocol'), Value: 'tag'
with open(sys.argv[2], 'r', newline='') as lookup_csv:
    reader = csv.DictReader(lookup_csv)
    for row in reader:
        tag_lookup.update({(row['dstport'], (str)(row['protocol'].lower())): (str)(row['tag']).lower()})
lookup_csv.close()

# Initialize a counter for untagged entries.
untagged = 0

# Open the flow log file and parse line-by-line.
with open(sys.argv[1], 'r') as flow_log:
    for log in flow_log:
        
        # Get destination port and protocol for current row.
        # I am using the default format for version 2 found here:
        # https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html
        
        log_data = log.split(' ')
        dstport = log_data[6]
        protocol = (str)(protocol_lookup[log_data[7]]).lower()

        # If this combination is already in port_protocol_matches,
        # increment its count by 1. Otherwise, add it.
        if (dstport, protocol) in port_protocol_matches:
            port_protocol_matches[(dstport, protocol)] += 1
        else:
            port_protocol_matches.update({(dstport, protocol): 1})

        # Use destination port and protocol to get the tag from
        # the lookup table.
        tag = tag_lookup.get((dstport, protocol), None)

        # If the tag is already in tag_matches, increment its
        # count by 1. Otherwise, add it. If the tag was not found,
        # the 'untagged' counter is incremented.
        if tag is not None:
            tag = (str)(tag).lower()
            if tag in tag_matches:
                tag_matches[tag] += 1
            else:
                tag_matches.update({tag: 1})
        else:
            untagged += 1

# Close the flow log file.
flow_log.close()

# Create output file.
with open('log_data_output', 'w') as output:
    
    # Write tag count output.
    output.write('Tag Counts:\nTag,Count\n')
    for tag, count in tag_matches.items():
        output.write(tag + ',' + (str)(count) + '\n')
    if untagged > 0:
        output.write('Untagged,' + (str)(untagged) + '\n')

    # Write port/protocol combination output.
    output.write('\nPort/Protocol Combination Counts:\nPort,Protocol,Count\n')
    for (port, protocol), count in port_protocol_matches.items():
        output.write((str)(port) + ',' + protocol + ',' + (str)(count) + '\n')

# Close output file.
output.close()