# Set up the directory hierarchy.
mkdir -p -m 740 "%{_datadir}/%{name}"
mkdir -p -m 700 "%{_datadir}/%{name}/.ssh"
chown olpcjournalprocessor:olpcjournalprocessor "%{_datadir}/%{name}" "%{_datadir}/%{name}/.ssh"

# If the key already exists, bail at this point.
if [ -f "%{_datadir}/%{name}/id_rsa" -o -f "%{_datadir}/%{name}/id_rsa.pub" ]; then
	exit 0
fi

# Generate an SSH key for the user.
ssh-keygen -C "olpcjournalprocessor remote access" -t rsa -f "%{_datadir}/%{name}/id_rsa" -N ""

echo -n "command=\"%{_bindir}/olpc-journal-processor\",no-port-forwarding,no-X11-forwarding,no-pty " >> "%{_datadir}/%{name}/.ssh/authorized_keys"
cat "%{_datadir}/%{name}/id_rsa.pub" >> "%{_datadir}/%{name}/.ssh/authorized_keys"

chmod 600 "%{_datadir}/%{name}/.ssh/authorized_keys" "%{_datadir}/%{name}/id_rsa" "%{_datadir}/%{name}/id_rsa.pub"
chown olpcjournalprocessor:olpcjournalprocessor "%{_datadir}/%{name}/.ssh/authorized_keys" "%{_datadir}/%{name}/id_rsa" "%{_datadir}/%{name}/id_rsa.pub"

exit 0
