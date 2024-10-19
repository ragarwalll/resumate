# Define the list of folders to be created
MODULE_FOLDERS := lib components

add-module:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Error: Module name not provided."; \
		echo "Usage: make add-module <module_name>"; \
		exit 1; \
	fi; \
	moduleName="$(filter-out $@,$(MAKECMDGOALS))"; \
	folderName=$$moduleName; \
	if [ -d "src/modules/$$folderName" ]; then \
		echo "Module '$$moduleName' already exists. Skipping folder creation."; \
	else \
		for folder in $(MODULE_FOLDERS); do \
			mkdir -p src/modules/$$folderName/$$folder; \
		done; \
		echo "Module '$$moduleName' folders created successfully."; \
	fi; \
	if jq -e '.compilerOptions.paths["@/module/'"$$folderName"'/*"]' tsconfig.json > /dev/null 2>&1; then \
		echo "Path for module '$$moduleName' already exists in tsconfig.json. Skipping update."; \
	else \
		jq '.compilerOptions.paths += {"@/module/'"$$folderName"'/*": ["./src/modules/'"$$folderName"'/*"]}' tsconfig.json > tsconfig.tmp.json && mv tsconfig.tmp.json tsconfig.json; \
		echo "Updated tsconfig.json with path for module '$$moduleName'."; \
	fi; \
	echo "Module '$$moduleName' processing completed."

%:
	@: