# Using Hashcat

Access the container:

    docker compose run --rm remote-interpreter bash

Then issue the command below to get the hash representation of the wallet:

    python utilities/bitcoin2john.py ./btcrecover/test/test-wallets/bitcoincore-wallet.dat > bitcoincore-wallet.hash

Output:

    $bitcoin$64$e6246120c45e390daa6a57476e7fbe4f57d83f79d75f9b4c1db680fe5a846cb8$16$4593aff5639179c7$67908$2$00$2$00

Check out the CUDA version by executing `nvidia-smi`. My driver supports the version `12.5`, so I used the image `dizcza/docker-hashcat:cuda12.1` because the latest version requires `12.8`:

```shell
docker run --network none --gpus all -it --rm --entrypoint sh \
--workdir /app \
--volume $(pwd):/app \
dizcza/docker-hashcat:cuda12.1 /bin/bash
```

Some examples showing how to crack the password:

```shell
# Simple mask example, but ignore the custom charset `abc`:
hashcat --status --hwmon-disable -m 11300 -a 3 -1 abc /app/bitcoincore-wallet.hash "btcr-test-password"
# Mask example with 4 custom charsets:
hashcat --hwmon-disable --status -m 11300 -a 3 \
-1 btcr \
-2 test \
-3 pass \
-4 word \
/app/bitcoincore-wallet.hash btc\?1-tes\?2-pa\?3\?3\?4\?4rd
# If you generated a password list, use it instead of the mask:
hashcat --hwmon-disable --status -m 11300 -a 0 /app/bitcoincore-wallet.hash /app/generated_password_list.txt
```

You'll see something like this:

```text
Session..........: hashcat                                
Status...........: Cracked
Hash.Mode........: 11300 (Bitcoin/Litecoin wallet.dat)
Hash.Target......: $bitcoin$64$e6246120c45e390daa6a57476e7fbe4f57d83f7...0$2$00
Time.Started.....: Thu May  1 22:34:51 2025 (1 sec)
Time.Estimated...: Thu May  1 22:34:52 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Mask.......: btcr-test-password [18]
Guess.Charset....: -1 abc, -2 Undefined, -3 Undefined, -4 Undefined 
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:        1 H/s (2.24ms) @ Accel:4 Loops:128 Thr:1024 Vec:1
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 1/1 (100.00%)
Rejected.........: 0/1 (0.00%)
Restore.Point....: 0/1 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: btcr-test-password -> btcr-test-password
Started: Thu May  1 22:34:33 2025
Stopped: Thu May  1 22:34:54 2025
```

You can check the cracked password in the [potfile](https://hashcat.net/wiki/doku.php?id=frequently_asked_questions#what_is_a_potfile):

    cat .local/share/hashcat/hashcat.potfile
