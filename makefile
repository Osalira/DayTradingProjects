# Define the list of project directories (adjust as necessary)
SERVICES = frontend-monolith backend/auth-service backend/trading-service backend/matching-engine backend/logging-service backend/api-gateway

# Default target: commit-all
commit-all:
	@echo "Starting commit process..."
	@# Check if the counter file exists; if not, initialize it to 0
	@if [ -f .commit_counter ]; then \
		count=$$(cat .commit_counter); \
	else \
		count=0; \
	fi; \
	newcount=$$((count+1)); \
	echo $$newcount > .commit_counter; \
	\
	# Determine ordinal suffix for the commit number
	suffix=$$( \
		case $$newcount in \
			1) echo "st";; \
			2) echo "nd";; \
			3) echo "rd";; \
			*) echo "th";; \
		esac); \
	\
	commit_msg="$$newcount$$suffix commit"; \
	echo "Using commit message: '$$commit_msg'" ; \
	\
	# Loop over each service directory and run git add/commit
	for dir in $(SERVICES); do \
		echo "Committing changes in $$dir..."; \
		( cd $$dir && git add . && git commit -m "$$commit_msg" ); \
	done
