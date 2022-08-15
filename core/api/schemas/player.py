class CreatePlayerRequestSchema(Schema):
    first_name = fields.String()
    last_name = fields.String()
    sex = fields.String()
    initial_evks_rating = fields.Integer(required=False)
    initial_evks_rank = EnumField(EvksPlayerRank, required=False)
    # TODO: validate initial_evks_rating and initial_evks_rank
