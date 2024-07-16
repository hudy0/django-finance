.PHONY: local
PRE_COMMIT = pre-commit

PRE_COMMIT_RUN = $(PRE_COMMIT) run --all-files

pre-commit:
	$(PRE_COMMIT_RUN)

fast_coverage:
	@echo "Running fast coverage check"
	@pytest --cov=django_finance -n 4 --dist loadfile -q

coverage:
	pytest --cov=django_finance --migrations -n 2 --dist loadfile