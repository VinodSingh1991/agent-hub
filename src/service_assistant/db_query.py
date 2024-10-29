GET_ALL_LEADS = "SELECT LeadID, FirstName, Amount, Email, Phone, CreatedBy FROM Leads"
GET_ACTION_ABLE_LEADS = "SELECT LeadID, FirstName, Amount, Email, Phone, CreatedBy FROM Leads where Amount > 200"
GET_TOP_PRIORITY_LEADS = "SELECT LeadID, FirstName, Amount, Email, Phone, CreatedBy, RatingId FROM Leads LIMIT 4 where RatingId > 2"

GET_ALL_ACCOUNTS = """SELECT 
    a.AccountId,
    a.FirstName,
    a.LastName,
    a.AccountType,
    a.Phone,
    a.Email,
    a.Address,
    o.OfferId,
    o.OfferName,
    o.OfferCriteria,
    o.MinIncome,
    c.CaseId,
    c.Subject AS CaseSubject,
    c.Status AS CaseStatus,
    d.DeptName AS DepartmentName
FROM 
    AcidAccount a
LEFT JOIN 
    AcidOffers o ON a.RelatedOffers = o.OfferId
LEFT JOIN 
    AcidCases c ON a.RelatedCases = c.CaseId
LEFT JOIN 
    AcidDepartment d ON c.DeptId = d.DeptId
ORDER BY 
    a.AccountId;"""

