# pySendMail

Simple python-based email client.

## Description

pySendMail is a (very) simple client for sending mails from the command line.
The mail body can be either read from a file or via stdin.
It supports multiple attachments.

## Configuration
Copy `config.json.example` to `config.json` and open it for editing.
In section `mail` enter the sender and receiver for the mail header.
In section `smtp` specify your SMTP server for outgoing mail transfer as well as your login credentials.

## Options
pySendMail supports the following command line options:

- `-h, --help`: show this help message and exit
- `-s SUBJECT, --subject`: SUBJECT mail subject
- `-f FILE, --file FILE`: mail content from file, specify `-` to read from stdin
- `-a ATTACH, --attach ATTACH`: attachment(s), can be specified multiple times
- `-r, --retry`: keep retrying until sending succeeds (except for failed logins)

## Examples
Send a simple hello, with "hello" as subject and "hello from pySendMail" as mail body:
```
echo "hello from pySendMail" | ./pySendMail -s "hello" -f-
```

Send multiple images:
```
./pySendMail -s "cat pics" -a cat1.png -a cat2.jpg
```

# License
[GPL v3](http://www.gnu.org/licenses/gpl.html)
(c) Alexander Heinlein

