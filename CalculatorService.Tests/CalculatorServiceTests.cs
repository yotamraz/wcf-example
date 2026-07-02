using WcfServiceLib;
using Xunit;

namespace CalculatorService.Tests;

public class CalculatorServiceTests
{
    private readonly WcfServiceLib.CalculatorService _svc = new();

    [Fact]
    public void Add_PositiveNumbers_ReturnsSum()
    {
        Assert.Equal(5.0, _svc.Add(2.0, 3.0));
    }

    [Fact]
    public void Add_WithZero_ReturnsSameNumber()
    {
        Assert.Equal(7.0, _svc.Add(7.0, 0.0));
    }

    [Fact]
    public void Add_NegativeNumbers_ReturnsNegativeSum()
    {
        Assert.Equal(-5.0, _svc.Add(-2.0, -3.0));
    }

    [Fact]
    public void Add_FloatingPoint_ReturnsCorrectResult()
    {
        Assert.Equal(26.5, _svc.Add(11.8, 14.7), precision: 10);
    }

    [Fact]
    public void Subtract_PositiveNumbers_ReturnsDifference()
    {
        Assert.Equal(1.0, _svc.Subtract(3.0, 2.0));
    }

    [Fact]
    public void Subtract_ToNegative_ReturnsNegativeResult()
    {
        Assert.Equal(-1.0, _svc.Subtract(2.0, 3.0));
    }

    [Fact]
    public void Subtract_FloatingPoint_ReturnsCorrectResult()
    {
        Assert.Equal(-2.9, _svc.Subtract(11.8, 14.7), precision: 10);
    }
}
