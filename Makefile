.PHONY: local

coverage:
	pytest --cov=journal --migrations -n 2 --dist loadfile

# fcov == "fast coverage" by skipping migrations checking. Save that for CI.
fcov:
	@echo "Running fast coverage check"
	@pytest --cov=journal -n 4 --dist loadfile -q