using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.Text.Json;
using System.IO;

namespace website.Controllers {
  public class TODController : Controller {

    [HttpGet("[controller]/all")]
    public IActionResult GetAll() {
      String jsonPath = Path.GetFullPath(Path.Combine("./Data/tod.json"));
      Console.WriteLine(jsonPath);
      string fullJson = System.IO.File.ReadAllText(jsonPath);

      //var jsonString = JsonSerializer.Deserialize(fullJson);
      //Console.WriteLine(jsonString);
      return Ok(fullJson);
    }

  }
}
