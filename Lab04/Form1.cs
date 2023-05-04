using System.ComponentModel;

namespace Lab4
{
    public partial class Form1 : Form
    {

        static List<Car> myCars = new(){
            new Car("E250", new Engine(1.8, 204, "CGI"), 2009),
            new Car("E350", new Engine(3.5, 292, "CGI"), 2009),
            new Car("A6", new Engine(2.5, 187, "FSI"), 2012),
            new Car("A6", new Engine(2.8, 220, "FSI"), 2012),
            new Car("A6", new Engine(3.0, 295, "TFSI"), 2012),
            new Car("A6", new Engine(2.0, 175, "TDI"), 2011),
            new Car("A6", new Engine(3.0, 309, "TDI"), 2011),
            new Car("S6", new Engine(4.0, 414, "TFSI"), 2012),
            new Car("S8", new Engine(4.0, 513, "TFSI"), 2012)
        };

        BindingSource carBindingSource;
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            MyBindingList<Car> myCarsBindingList = new MyBindingList<Car>(myCars);
            carBindingSource = new BindingSource();
            carBindingSource.DataSource = myCarsBindingList;
            //Drag a DataGridView control from the Toolbox to the form.
            dataGridView1.DataSource = carBindingSource;
            loadProperties(((ITypedList)carBindingSource).GetItemProperties(null));
            searchInText.SelectedIndex = 0;

            Exercise1();
            Exercise2();
        }

        private void loadProperties(PropertyDescriptorCollection collection)
        {
            foreach (PropertyDescriptor property in collection)
            {
                if (property.PropertyType == typeof(Int32) ||
                    property.PropertyType == typeof(string))
                {
                    searchInText.Items.Add(property.Name);
                }
                else
                {
                    //loadProperties(property.GetChildProperties());
                }

            }
        }

        private static void Exercise1()
        {

            var elements = from engineTypes in (
                           from car in myCars
                           where car.Model == "A6"
                           select new
                           {
                               engineType = car.Motor.Model.Contains("TDI") ? "diesel" : "petrol",
                               hppl = car.Motor.HorsePower / car.Motor.Displacement
                           })
                           group engineTypes by engineTypes.engineType into groupedEngineTypes
                           select new
                           {
                               engineType = groupedEngineTypes.Key,
                               avgHPPL = groupedEngineTypes.Average(x => x.hppl)
                           } into sortedEngineTypes
                           orderby sortedEngineTypes.avgHPPL descending
                           select sortedEngineTypes;

            foreach (var e in elements) Console.WriteLine(e.engineType + ": " + e.avgHPPL);

            var elements2 = myCars.AsEnumerable().
                Where(car => car.Model == "A6").
                    Select(car => new
                    {
                        engineType = car.Motor.Model.Contains("TDI") ? "diesel" : "petrol",
                        hppl = car.Motor.HorsePower / car.Motor.Displacement
                    }).
                    GroupBy(x => x.engineType).
                    Select(type => new
                    {
                        engineType = type.Key,
                        avgHPPL = type.Average(x => x.hppl)
                    }).
                    OrderByDescending(x => x.avgHPPL);

            foreach (var e in elements2) Console.WriteLine(e.engineType + ": " + e.avgHPPL);

        }

        private static int SortDescendingByHorsePower(Car car1, Car car2)
        {
            return car2.Motor.CompareTo(car1.Motor);
        }

        private static bool CheckIfTDI(Car car)
        {
            return car.Motor.Model.Equals("TDI");
        }

        private static void DisplayResult(Car car)
        {
            MessageBox.Show($"{car.Model} {car.Motor} {car.Year}", "Result");

        }

        private static void Exercise2()
        {

            Func<Car, Car, int> arg1 = SortDescendingByHorsePower;
            Predicate<Car> arg2 = CheckIfTDI;
            Action<Car> arg3 = DisplayResult;

            myCars.Sort(new Comparison<Car>(arg1));
            myCars.FindAll(arg2).ForEach(arg3);
        }

        private void findButton_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(searchForText.Text) ||
                string.IsNullOrEmpty(searchInText.Text)) return;

            PropertyDescriptorCollection properties = ((ITypedList)carBindingSource).GetItemProperties(null);
            PropertyDescriptor property = properties[searchInText.Text];

            int index = carBindingSource.Find(property, searchForText.Text);

            if (index != -1)
            {
                carBindingSource.Position = index;
            }
            else
            {
                MessageBox.Show("Not found");
            }

        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            var senderGrid = (DataGridView)sender;

            if (senderGrid.Columns[e.ColumnIndex] is DataGridViewButtonColumn &&
                e.RowIndex >= 0 && carBindingSource.Count > 0)
            {
                carBindingSource.RemoveAt(e.RowIndex);
            }

        }

        private void dataGridView1_DataError(object sender, DataGridViewDataErrorEventArgs e)
        {
            dataGridView1.Rows[e.RowIndex].ErrorText = $"Wrong value at ({e.RowIndex},{e.ColumnIndex})";
            e.Cancel = true;
        }

        private void dataGridView1_CellParsing(object sender, DataGridViewCellParsingEventArgs e)
        {
            dataGridView1.Rows[e.RowIndex].ErrorText = "";
            if (this.dataGridView1.Columns[e.ColumnIndex].Name == "Motor")
            {
                if (e != null)
                {
                    if (e.Value != null)
                    {
                        try
                        {
                            string[] entry = e.Value.ToString().Split(" ");
                            if (entry.Length < 2) { throw new FormatException(); }
                            e.Value = new Engine(double.Parse(entry[1]), double.Parse(entry[2]), entry[0]);


                            e.ParsingApplied = true;
                        }
                        catch (FormatException)
                        {
                            MessageBox.Show("Use {Model} {Displacement} {HorsePower}", "Wrong format");

                            e.ParsingApplied = false;
                        }
                    }
                }
            }
        }

    }
}