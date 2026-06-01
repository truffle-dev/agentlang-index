# Vendored Zero snapshots

Each subdirectory is a pinned snapshot of a Zero release: the
`zero --version` output plus the bundled skill data from
`zero skills get <name> --full`. The `CURRENT` symlink points at
the snapshot the harness should use for new benchmark runs.

Between Zero release tags, `version.txt` records the upstream
commit SHA that the corpus and CI are pinned to. `bin/zero --version`
does not report a SHA on its own (the field reads `commit: unknown`),
so the SHA is captured manually from `git rev-parse HEAD` against
the Zero clone. `.github/workflows/verify-refs.yml` pins the same
SHA so CI and local development agree.

To refresh:

```sh
ZERO=~/repos/zero/bin/zero
VERSION=$($ZERO --version | head -1 | awk '{print $2}')
SHA=$(git -C ~/repos/zero rev-parse HEAD)
SHA_DATE=$(git -C ~/repos/zero log -1 --format='%cI' | sed 's/+.*//')
mkdir -p $VERSION
for skill in zero-language zero-diagnostics zero-stdlib zero-agent zero-builds zero-packages zero-testing; do
  $ZERO skills get $skill --full > $VERSION/skill-$skill.md
  $ZERO skills get $skill --full --json > $VERSION/skill-$skill.json
done
$ZERO --version | sed "s/^commit: unknown/commit: $SHA\ncommit-date: ${SHA_DATE}Z/" > $VERSION/version.txt
rm -f CURRENT && ln -s $VERSION CURRENT
```

Snapshots are kept indefinitely so old benchmark runs remain reproducible.
