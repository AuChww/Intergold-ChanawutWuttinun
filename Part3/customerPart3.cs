using System.Data;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json.Linq;
using System.Data.SqlClient;

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

        if (!startDate.HasValue)
            startDate = new DateTime(1950, 1, 1); 

        if (!endDate.HasValue)
            endDate = DateTime.Now; 

        sql += " AND created_at BETWEEN @start AND @end";
        cmd.Parameters.Add("@start", SqlDbType.DateTime).Value = startDate.Value;
        cmd.Parameters.Add("@end", SqlDbType.DateTime).Value = endDate.Value;

        cmd.CommandText = sql;

        using (var da = new SqlDataAdapter(cmd))
        {
            da.Fill(dt);
        }
    }

    return dt;
}
