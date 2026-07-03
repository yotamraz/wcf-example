using CoreWCF;
using CoreWCF.Configuration;
using CoreWCF.Description;
using WcfServiceLib;

var builder = WebApplication.CreateBuilder(args);
builder.WebHost.UseUrls("http://localhost:8080");

builder.Services.AddServiceModelServices();
builder.Services.AddServiceModelMetadata();
builder.Services.AddSingleton<CalculatorService>();

var app = builder.Build();

app.UseServiceModel(serviceBuilder =>
{
    serviceBuilder.AddService<CalculatorService>();
    serviceBuilder.AddServiceEndpoint<CalculatorService, ICalculatorService>(
        new BasicHttpBinding(), "/CalculatorService");

    var serviceMetadataBehavior = app.Services.GetRequiredService<ServiceMetadataBehavior>();
    serviceMetadataBehavior.HttpGetEnabled = true;
});

Console.WriteLine("The service is ready at http://localhost:8080/CalculatorService");
app.Run();

public partial class Program { }
