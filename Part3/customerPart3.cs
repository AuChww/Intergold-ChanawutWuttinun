using System.Data;
using Microsoft.Extensions.Configuration;

public DataTable GetCustomerInfo(string id, DateTime? startDate = null, DateTime? endDate = null)
{
    var dt = new DataTable();
    
    var config = JsonConvert.DeserializeObject<JObject>(File.ReadAllText("appsettings.json"));
    var dbConfig = config["ConnectionStrings"]["DefaultConnection"];

    using (var conn = new SqlConnection(
        $"Server={dbConfig["host"]};Database={dbConfig["database"]};User Id={dbConfig["user"]};Password={dbConfig["password"]};"))
    {
        conn.Open();
        string sql = "SELECT id, name, email FROM Customer WHERE id = @id";
        var cmd = new SqlCommand();
        cmd.Connection = conn;
        cmd.Parameters.AddWithValue("@id", id);

        if (!string.IsNullOrEmpty(startDate))
        {
            if (string.IsNullOrEmpty(endDate))
            {
                endDate = DateTime.Now.ToString("dd-MM-yyyy");
            }
            sql += " AND created_at BETWEEN @start AND @end";
            cmd.Parameters.AddWithValue("@start", startDate);
            cmd.Parameters.AddWithValue("@end", endDate);
        }

        cmd.CommandText = sql;
        using (var da = new SqlDataAdapter(cmd))
        {
            da.Fill(dt);
        }
    }
    return dt;
}

