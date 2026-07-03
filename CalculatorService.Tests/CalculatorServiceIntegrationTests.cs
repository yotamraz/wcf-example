using System.ServiceModel;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Hosting.Server;
using Microsoft.AspNetCore.Hosting.Server.Features;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;
using ServiceReference1;
using Xunit;

namespace CalculatorService.Tests;

/// <summary>
/// Integration tests that spin up the CoreWCF host via WebApplicationFactory
/// using a real Kestrel listener on a dynamic port, then call it through the
/// generated CalculatorServiceClient proxy.
/// </summary>
public class CalculatorServiceIntegrationTests : IClassFixture<CalculatorServiceIntegrationTests.WcfTestFactory>
{
    /// <summary>
    /// Custom WebApplicationFactory that configures Kestrel to listen on a
    /// dynamically assigned port (port 0) so that the WCF client can make a
    /// real TCP connection to the in-process server.
    /// </summary>
    public class WcfTestFactory : WebApplicationFactory<Program>
    {
        protected override void ConfigureWebHost(IWebHostBuilder builder)
        {
            builder.UseEnvironment("Development");
            // Override the hardcoded UseUrls from Program.cs with a dynamic port.
            builder.UseUrls("http://127.0.0.1:0");
        }

        /// <summary>
        /// Returns the actual port the server bound to after startup.
        /// </summary>
        public int GetPort()
        {
            // Ensure the server is started by accessing it.
            _ = Server;
            var addressFeature = Server.Services.GetRequiredService<IServer>()
                .Features.Get<IServerAddressesFeature>();
            var address = addressFeature!.Addresses.First();
            return new Uri(address).Port;
        }
    }

    private readonly WcfTestFactory _factory;

    public CalculatorServiceIntegrationTests(WcfTestFactory factory)
    {
        _factory = factory;
    }

    private CalculatorServiceClient CreateClient()
    {
        var port = _factory.GetPort();
        var binding = new BasicHttpBinding();
        var endpointAddress = new EndpointAddress(
            new Uri($"http://127.0.0.1:{port}/CalculatorService"));
        return new CalculatorServiceClient(binding, endpointAddress);
    }

    private static async Task CloseClientAsync(CalculatorServiceClient client)
    {
        try
        {
            await client.CloseAsync();
        }
        catch
        {
            client.Abort();
        }
    }

    [Fact]
    public async Task Add_ReturnsCorrectSum()
    {
        var client = CreateClient();
        try
        {
            var result = await client.AddAsync(11.8, 14.7);
            Assert.Equal(26.5, result, precision: 10);
        }
        finally
        {
            await CloseClientAsync(client);
        }
    }

    [Fact]
    public async Task Subtract_ReturnsCorrectDifference()
    {
        var client = CreateClient();
        try
        {
            var result = await client.SubtractAsync(11.8, 14.7);
            Assert.Equal(-2.9, result, precision: 10);
        }
        finally
        {
            await CloseClientAsync(client);
        }
    }
}
