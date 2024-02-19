def test_load_data():
    from Analysis import Analysis
    my_instance = Analysis()
    
    my_instance.load_data()
    
    my_instance.compute_analysis()
    
    my_instance.plot_data()
    
    my_instance.notify_done("Test Finished!")
    
    assert True