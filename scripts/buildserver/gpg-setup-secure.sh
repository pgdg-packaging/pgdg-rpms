#!/usr/bin/bash

#########################################################
#							#
# Secure GPG Agent Setup for Automated Signing		#
# Devrim Gündüz <devrim@gunduz.org> - 2026		#
#							#
#########################################################

# This script sets up GPG agent for automated signing
# More secure than using expect scripts

# 1. Configure gpg-agent (add to ~/.gnupg/gpg-agent.conf)
setup_gpg_agent() {
    local GPG_AGENT_CONF="$HOME/.gnupg/gpg-agent.conf"

    cat > "$GPG_AGENT_CONF" <<EOF
# Cache settings for automated signing
default-cache-ttl 345600
max-cache-ttl 345600

# Allow preset passphrases
allow-preset-passphrase

# Pinentry mode for unattended operations
pinentry-program /usr/bin/pinentry-tty
EOF

    chmod 600 "$GPG_AGENT_CONF"
    echo "GPG agent configuration updated"
}

# 2. Restart GPG agent to apply new settings
restart_gpg_agent() {
    gpgconf --kill gpg-agent
    gpg-agent --daemon
    echo "GPG agent restarted"
}

# 3. Preset the passphrase for your signing key
preset_passphrase() {
    local GPG_KEY_GRIP="$1"
    local GPG_PASSWORD="$2"

    # Get the keygrip if not provided
    if [ -z "$GPG_KEY_GRIP" ]; then
        echo "Getting keygrip for default signing key..."
        GPG_KEY_GRIP=$(gpg --with-keygrip -K | grep -A 1 "ssb" | grep "Keygrip" | head -1 | awk '{print $3}')
    fi

    if [ -z "$GPG_KEY_GRIP" ]; then
        echo "ERROR: Could not determine keygrip. Please provide it manually."
        return 1
    fi

    echo "Presetting passphrase for keygrip: $GPG_KEY_GRIP"

    # Preset the passphrase (valid for the cache TTL period)
    echo "$GPG_PASSWORD" | /usr/libexec/gpg-preset-passphrase --preset "$GPG_KEY_GRIP"
 
    if [ $? -eq 0 ]; then
        echo "Passphrase preset successfully"
        return 0
    else
        echo "ERROR: Failed to preset passphrase"
        return 1
    fi
}

# Main setup function
main() {
    echo "Setting up secure GPG agent for automated signing..."

    setup_gpg_agent
    restart_gpg_agent

    # Note: You need to call preset_passphrase with your key's keygrip
    # Find your keygrip with: gpg --with-keygrip -K

    echo ""
    echo "Setup complete!"
    echo ""
    echo "To preset your passphrase, run:"
    echo "  /usr/libexec/gpg-preset-passphrase --preset <KEYGRIP>"
    echo ""
    echo "Find your keygrip with:"
    echo "  gpg --with-keygrip -K"
}

# Run main if executed directly
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main
fi
