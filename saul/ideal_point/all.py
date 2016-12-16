from . import raw_data, ideal_point, gradient


def all_(learn_points=False, legislator_df=None, bill_df=None, sponsor_df=None, vote_df=None, position_df=None):
	"""
	If `learn_points` will perform gradient descent to get ideal points. Else 
	will from disk.


	Returns:

	legislator_df, bill_df, sponsor_df, vote_df, position_df
	"""
	if not legislator_df:
		legislator_df = raw_data.legislators()
	if not bill_df or not sponsor_df:
		bill_df, sponsor_df = raw_data.bills(legislator_df)
	if not vote_df or not position_df:
		vote_df, position_df = raw_data.votes(legislator_df, bill_df)
	model_position_df, model_legislator_index, model_vote_index = ideal_point.transform_data(position_df, vote_df, legislator_df)
	if learn_points:
		g = gradient.Gradient(model_position_df)
		g.run(1000)
		params = g.params
		ideal_point.ideal_point.save_params(params)
	else:
		params = ideal_point.load_params()
	legislator_pt_df = ideal_point.leg_add_ideology(legislator_df, model_legislator_index, params)
	vote_pt_df = ideal_point.vote_add_ideology_and_bias(vote_df, model_vote_index, params)
	return legislator_pt_df, bill_df, sponsor_df, vote_pt_df, position_df
