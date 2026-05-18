# Vendored Zero snapshots

Each subdirectory is a pinned snapshot of a Zero release: the
`zero --version` output plus the bundled skill data from
`zero skills get <name> --full`. The `CURRENT` symlink points at
the snapshot the harness should use for new benchmark runs.

To refresh:

```sh
ZERO=~/repos/zero/bin/zero
VERSION=$($ZERO --version | head -1 | awk '{print $2}')
mkdir -p $VERSION
for skill in zero-language zero-diagnostics zero-stdlib zero-agent zero-builds zero-packages zero-testing; do
  $ZERO skills get $skill --full > $VERSION/skill-$skill.md
  $ZERO skills get $skill --full --json > $VERSION/skill-$skill.json
done
rm -f CURRENT && ln -s $VERSION CURRENT
```

Snapshots are kept indefinitely so old benchmark runs remain reproducible.
