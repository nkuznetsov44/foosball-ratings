from core.api.schemas.tournament import CreateTournamentRequestSchema, TournamentResponseSchema


class TournamentView:
    @request_schema(CreateTournamentRequestSchema())
    @response_schema(TournamentResponseSchema())
    def post(self):
        pass
