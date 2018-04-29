import paralleldots

paralleldots.get_api_key()

test_sim=paralleldots.similarity( "computer dead", "computer dead" )
score=test_sim["actual_score"]
print(score)  # Test
