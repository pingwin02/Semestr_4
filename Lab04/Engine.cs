using System.Xml.Serialization;

namespace Lab4
{
    public class Engine : IComparable
    {
        public double Displacement { get; set; }
        public double HorsePower { get; set; }
        [XmlAttribute(AttributeName = "model")]
        public string Model { get; set; }

        public Engine() { }
        public Engine(double displacement, double horsePower, string model)
        {
            this.Displacement = displacement;
            this.HorsePower = horsePower;
            this.Model = model;
        }

        public override string ToString()
        {
            return $"{Model} {Displacement} ({HorsePower} hp)";
        }
        public int CompareTo(object other)
        {
            Engine otherEngine = (Engine)other;
            return HorsePower.CompareTo(otherEngine.HorsePower);
        }

    }
}
