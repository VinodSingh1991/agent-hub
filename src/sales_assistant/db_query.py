GET_ALL_LEADS = "SELECT LeadID, FirstName, Amount, Email, Phone, CreatedBy FROM Leads"
GET_ACTION_ABLE_LEADS = "SELECT LeadID, FirstName, Amount, Email, Phone, CreatedBy FROM Leads where Amount > 200"
GET_TOP_PRIORITY_LEADS = "SELECT LeadID, FirstName, Amount, Email, Phone, CreatedBy, RatingId FROM Leads LIMIT 4 where RatingId > 2"