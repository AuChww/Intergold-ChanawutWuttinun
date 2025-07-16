

public DataTable GetCustomerInfo(string id)
{
    var dt = new DataTable();
    using (var conn = new SqlConnection("...")) // Connection string is hardcoded
    {
    conn.Open();
    var sql = "SELECT * FROM Customer WHERE id = @id";
    using (var da = new SqlDataAdapter(sql, conn))
    {
    da.Fill(dt);
    }
    }
    return dt;
}