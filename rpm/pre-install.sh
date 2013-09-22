# Add a nologin olpcjournalprocessor user and group.
getent group olpcjournalprocessor >/dev/null || groupadd -r olpcjournalprocessor
getent passwd olpcjournalprocessor >/dev/null || \
    useradd -r -g olpcjournalprocessor -d  %{_datadir}/%{name} -s /bin/bash \
    -c "SSH-only user for remotely processing Journal statistics" olpcjournalprocessor

exit 0
