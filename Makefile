# Offline by default: docs regenerate from data/numbers.json + merge-kit profiles + src/ + notes/.
# `make collect` re-reads the observatory outputs (OBSERVATORY=path, default ../contrib-observatory).
PY := python3 -I
DOCS := README.md STATE-OF-THE-FIELD.md FAILURE-MODES.md PLAYBOOK.md LIMITS.md REPOS/*.md

all: docs privacy

docs:
	$(PY) scripts/repo_pages.py
	$(PY) scripts/stamp.py --lint

collect:
	$(PY) scripts/collect_numbers.py

privacy:
	$(PY) scripts/privacy_check.py

selftest:
	cd merge-kit && ./merge-kit selftest

# two clean builds must give byte-identical docs
check: selftest
	rm -rf src/REPOS REPOS $(filter-out REPOS/*.md,$(DOCS)) && $(MAKE) -s docs >/dev/null && sha256sum $(DOCS) > .run1.sums
	rm -rf src/REPOS REPOS $(filter-out REPOS/*.md,$(DOCS)) && $(MAKE) -s docs >/dev/null && sha256sum $(DOCS) > .run2.sums
	cmp .run1.sums .run2.sums && echo "DETERMINISM: identical" && rm -f .run1.sums .run2.sums
	$(MAKE) -s privacy

# network, optional: TauCetiReview's open rubrics for merge-kit's llm-pass-prompt.md
rubrics:
	d=$$(mktemp -d) && git clone -q --depth 1 https://github.com/TauCetiProject/TauCetiReview $$d/r && \
	  rm -rf merge-kit/rubrics && cp -r $$d/r/rubrics merge-kit/rubrics && rm -rf $$d

.PHONY: all docs collect privacy selftest check rubrics
