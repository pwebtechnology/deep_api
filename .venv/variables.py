from datetime import datetime, timedelta, date

props = {
    'startDate': '2023-08-28',
    'endDate': '2023-12-28',
    'affiliates': ['Scale', 'VectorMedia'],
    'divider': 'week'
}

utcDateFormat = "%Y-%m-%d"
rev_format = "%d.%m.%y"
mongo_uri = "mongodb://NikKimp:NikKimp@172.23.2.15:27017/?tls=false&authMechanism=DEFAULT"

unassignedStages = ['Empty Empty', 'Empty', 'System Tech', 'Arthur Ray', 'Natasha Romanova']

empty_date = "1970-01-01 00:00:00";

affilateException = {
    'Diamond': ['DIAMOND'],
    'MGA': ['MGAautsp'],
    'Scale': ['ScaleCA', 'ScaleAUtsp'],
}


def queryConvCompare(props):
    affiliates = props['affiliates']
    startDate = props['startDate']
    endDate = props['endDate']
    startDate = datetime.strptime(startDate, utcDateFormat)
    endDate = datetime.strptime(endDate, utcDateFormat)
    return [
        {"$addFields": {"Affiliate": {"$arrayElemAt": [{"$split": ["$Campaign_Campaign_Name", "_"]}, 0]}}},
        {"$match": {
            "Trader_Sale_Status": {"$ne": "Test"},
            "Affiliate": {"$in": affiliates},
            "$or": [
                {
                    "Trader_Ftd_Date": {
                        "$gte": startDate,
                        "$lt": endDate,
                    }
                },
                {
                    "Trader_Registered_At": {
                        "$gte": startDate,
                        "$lt": endDate,
                    }
                },
            ]
        }}
    ]

def queryConvCompareBuilder(props):
    startDate = props['startDate']
    endDate = props['endDate']
    startDate = datetime.strptime(startDate, utcDateFormat)
    endDate = datetime.strptime(endDate, utcDateFormat)
    return [
        {"$match": {
            "Trader_Sale_Status": {"$ne": "Test"},
            "$or": [
                {
                    "Trader_Ftd_Date": {
                        "$gte": startDate,
                        "$lt": endDate,
                    }
                },
                {
                    "Trader_Registered_At": {
                        "$gte": startDate,
                        "$lt": endDate,
                    }
                },
            ]
        }}
    ]



def queryRetCompare(props):
    affiliates = props['affiliates']
    startDate = props['startDate']
    endDate = props['endDate']
    startDate = datetime.strptime(startDate, utcDateFormat)
    endDate = datetime.strptime(endDate, utcDateFormat)
    finishedAffilatesList = []

    for affilate in affiliates:
        if affilate in affilateException:
            finishedAffilatesList.extend(affilateException[affilate])
        finishedAffilatesList.append(affilate)
    return [
        {"$addFields": {"Affiliate": {"$arrayElemAt": [{"$split": ["$Campaign_Name", "_"]}, 0]}}},
        {"$match": {
            "Affiliate": {"$in": finishedAffilatesList},
            "Ticket_Method": {"$ne": "Qiwi"},
            "Ticket_Status": "Approved",
            "Desk_Desk_Name": {"$ne": "Test"},
            "$or": [
                {
                    "Trader_Ftd_Date": {
                        "$gte": startDate,
                        "$lt": endDate,
                    }
                },
                {
                    "Ticket_Created_At": {
                        "$gte": startDate,
                        "$lt": endDate,
                    }
                },
            ]}
        }
    ]


def queryRetCompareBuilder(props):
    startDate = props['startDate']
    endDate = props['endDate']
    startDate = datetime.strptime(startDate, utcDateFormat)
    endDate = datetime.strptime(endDate, utcDateFormat)

    return [
        {"$match": {
            "Ticket_Method": {"$ne": "Qiwi"},
            "Ticket_Status": "Approved",
            "Desk_Desk_Name": {"$ne": "Test"},
            "$or": [
                {
                    "Trader_Ftd_Date": {
                        "$gte": startDate,
                        "$lt": endDate,
                    }
                },
                {
                    "Ticket_Created_At": {
                        "$gte": startDate,
                        "$lt": endDate,
                    }
                },
            ]}
        }
    ]

def paymentsQuery(props):
    affilateList = props['affiliates']
    startDate = props['startDate']
    endDate = props['endDate']

    return [
        {
            "$match": {
                "affiliate": {"$in": affilateList},
                "date": {
                    "$gte": startDate,
                    "$lte": endDate
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "date": 1,
                "affiliate": 1,
                "payment": {"$toDouble": "$amount_of_payment"}
            }
        },
        {
            "$sort": {
                "date": -1
            }
        }
    ]

def paymentsQueryBuilder(props):
    affilateList = props['affiliates']
    startDate = props['startDate']
    endDate = props['endDate']

    return [
        {
            "$match": {
                "affiliate": {"$in": affilateList},
                "date": {
                    "$gte": startDate,
                    "$lte": endDate
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "date": 1,
                "affiliate": 1,
                "payment": {"$toDouble": "$amount_of_payment"}
            }
        },
        {
            "$sort": {
                "date": -1
            }
        }
    ]



prev_day = date.today() - timedelta(1)
previous_day_date = datetime.combine(prev_day, datetime.max.time())
previous_day_date_str = prev_day.strftime("%Y-%m-%d")

print(previous_day_date)

conv_parameters = {
    'database': "admin",
    'queryAll': [
        {
            "$addFields": {
                "Affiliate": {"$arrayElemAt": [{"$split": ["$Campaign_Campaign_Name", "_"]}, 0]}
            }
        },
        {
            "$match": {
                "Trader_Sale_Status": {"$ne": 'Test'}
            }
        },
    ],
    'query': queryConvCompare,
    'queryPrevDay': [
        {
            "$addFields": {
                "Affiliate": {"$arrayElemAt": [{"$split": ["$Campaign_Campaign_Name", "_"]}, 0]}
            }
        },
        {
            "$match": {
                "Trader_Sale_Status": {"$ne": 'Test'},
                "$or": [
                    {
                        "Trader_Ftd_Date": {
                            "$lt": previous_day_date,
                        }
                    },
                    {
                        "Trader_Registered_At": {
                            "$lt": previous_day_date,
                        }
                    },
                ],
                "Trader_Ftd_Date": {"$ne": "Empty"},
                "Trader_Registered_At": {"$ne": "Empty"},
            }
        },
    ],
}

conv_parameters_builder = {
    'database': "admin",
    'queryAll': [
        {
            "$match": {
                "Trader_Sale_Status": {"$ne": 'Test'}
            }
        },
    ],
    'query': queryConvCompareBuilder,
    'queryPrevDay': [

        {
            "$match": {
                "Trader_Sale_Status": {"$ne": 'Test'},
                "$or": [
                    {
                        "Trader_Ftd_Date": {
                            "$lt": previous_day_date,
                        }
                    },
                    {
                        "Trader_Registered_At": {
                            "$lt": previous_day_date,
                        }
                    },
                ],
                "Trader_Ftd_Date": {"$ne": "Empty"},
                "Trader_Registered_At": {"$ne": "Empty"},
            }
        },
    ],
}



ret_parameters = {
    'database': "retention",
    'queryPrevDay': [
        {
            "$addFields": {
                "Affiliate": {"$arrayElemAt": [{"$split": ["$Campaign_Name", "_"]}, 0]}
            }
        },
        {
            "$match": {
                "Ticket_Method": {"$ne": "Qiwi"},
                "Ticket_Status": "Approved",
                "Desk_Desk_Name": {"$ne": "Test"},
                "$or": [
                    {
                        "Trader_Ftd_Date": {
                            "$lt": previous_day_date,
                        }
                    },
                    {
                        "Ticket_Created_At": {
                            "$lt": previous_day_date,
                        }
                    },
                ],
                "Trader_Ftd_Date": {"$ne": "Empty"},
                "Ticket_Created_At": {"$ne": "Empty"},
            }
        },
    ],
    'query': queryRetCompare,
    'queryAll': [
        {
            "$addFields": {
                "Affiliate": {"$arrayElemAt": [{"$split": ["$Campaign_Name", "_"]}, 0]}
            }
        },
        {
            "$match": {
                "Ticket_Method": {"$ne": "Qiwi"},
                "Ticket_Status": "Approved",
                "Desk_Desk_Name": {"$ne": "Test"},
            }
        },
    ],
}


ret_parameters_builder = {
    'database': "retention",
    'queryPrevDay': [

        {
            "$match": {
                "Ticket_Method": {"$ne": "Qiwi"},
                "Ticket_Status": "Approved",
                "Desk_Desk_Name": {"$ne": "Test"},
                "$or": [
                    {
                        "Trader_Ftd_Date": {
                            "$lt": previous_day_date,
                        }
                    },
                    {
                        "Ticket_Created_At": {
                            "$lt": previous_day_date,
                        }
                    },
                ],
                "Trader_Ftd_Date": {"$ne": "Empty"},
                "Ticket_Created_At": {"$ne": "Empty"},
            }
        },
    ],
    'query': queryRetCompareBuilder,
    'queryAll': [

        {
            "$match": {
                "Ticket_Method": {"$ne": "Qiwi"},
                "Ticket_Status": "Approved",
                "Desk_Desk_Name": {"$ne": "Test"},
            }
        },
    ],
}

payment_parametrs = {
    'database': "aff_balance",
    'queryAll': [
        {
            "$group": {
                "_id": "$affiliate",
                "payment": {"$sum": {"$toDouble": "$amount_of_payment"}}
            }
        },
        {
            "$project": {
                "_id": 0,
                "affiliate": "$_id",
                "payment": 1
            }
        }
    ],
    'query': paymentsQuery,
    'queryPrevDay': [
        {
            "$match": {
                "date": {
                    "$lte": previous_day_date_str
                }
            }
        },
        {
            "$group": {
                "_id": "$affiliate",
                "payment": {"$sum": {"$toDouble": "$amount_of_payment"}}
            }
        },
        {
            "$project": {
                "_id": 0,
                "affiliate": "$_id",
                "payment": 1
            }
        }
    ],
}

payment_parametrs_builder = {
    'database': "aff_balance",
    'queryAll': [
        {
            "$group": {
                "_id": "$affiliate",
                "payment": {"$sum": {"$toDouble": "$amount_of_payment"}}
            }
        },
        {
            "$project": {
                "_id": 0,
                "affiliate": "$_id",
                "payment": 1
            }
        }
    ],
    'query': paymentsQueryBuilder,
    'queryPrevDay': [
        {
            "$match": {
                "date": {
                    "$lte": previous_day_date_str
                }
            }
        },
        {
            "$group": {
                "_id": "$affiliate",
                "payment": {"$sum": {"$toDouble": "$amount_of_payment"}}
            }
        },
        {
            "$project": {
                "_id": 0,
                "affiliate": "$_id",
                "payment": 1
            }
        }
    ],
}







payment_collection = ['payments']
conv_collections = ["traders_data_crm", "traders_data_crm_bestinvest", "traders_data_crm_pulsetrade","traders_data_origintarget","traders_data_triumphwhite"]
ret_collections = ['tickets_data_crm_beglobalfund',
                   'tickets_data_crm_call4trade',
                   'tickets_data_crm_capitalbmarket',
                   'tickets_data_crm_fxmargine',
                   'tickets_data_crm_goldnrise',
                   'tickets_data_crm_insidethefund',
                   'tickets_data_crm_intrafund',
                   'tickets_data_crm_mytrademate',
                   'tickets_data_crm_onetouchinvest',
                   'tickets_data_crm_rockstonetrust',
                   'tickets_data_crm_timemarkets2',
                   'tickets_data_crm_tlcvstments',
                   'tickets_data_crm_trademay',
                   'tickets_data_crm_titangap',
                   'tickets_data_crm_tradeonyx',
                   "tickets_data_crm_triumphincome",
                   "tickets_data_crm_traderminds5",
                   "tickets_data_crm_thebiggestfuture",
                   "tickets_data_crm_suntrustltd",
                   "tickets_data_crm_spidertrex",
                   "tickets_data_crm_solaris",
                   "tickets_data_crm_skytargetltd",
                   "tickets_data_crm_rockstonetrust",
                   "tickets_data_crm_robintrov",
                   "tickets_data_crm_reinholdsgold",
                   "tickets_data_crm_introode",
                   "tickets_data_crm_goldentargets",
                   "tickets_data_crm_astronixfund"]
