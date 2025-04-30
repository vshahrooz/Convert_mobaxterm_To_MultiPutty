# Convert_mobaxterm_To_MultiPutty
Convert Backup MobaXterm.mobaconf  To MultiPutty XML Importer

This script converts MobaXterm session backups (stored in the MobaXterm.mobaconf file) into a format that can be imported into MTPuTTY (Multi PuTTY Manager), which uses XML format for its session list.

The script extracts only the SSH and Telnet sessions from the .mobaconf file, preserving information such as:

Session name

IP address or hostname

Port number

Protocol type (SSH/Telnet)

The resulting file is a valid XML file compatible with MTPuTTY, making it easy to migrate sessions between MobaXterm and MTPuTTY.
