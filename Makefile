compose:
	@docker compose --profile ui --profile server up --build

compose-ui:
	@docker compose --profile ui up --build

compose-server:
	@docker compose --profile server up --build

.PHONY: compose compose-ui compose-server