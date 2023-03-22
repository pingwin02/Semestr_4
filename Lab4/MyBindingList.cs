using System.Collections;
using System.ComponentModel;
using System.Reflection;

namespace Lab4
{
    internal class MyBindingList<T> : BindingList<T>
    {
        private bool _isSorted;
        public MyBindingList() : base() { }
        public MyBindingList(IList<T> list) : base(list) { }

        internal class PropertyComparer<T> : Comparer<T>
        {
            private PropertyDescriptor _property;
            private ListSortDirection _direction;
            private IComparer _comparer;
            internal PropertyComparer(PropertyDescriptor prop, ListSortDirection direction)
            {
                _property = prop;
                _direction = direction;

                Type comparerType = typeof(Comparer<>).MakeGenericType(prop.PropertyType);
                PropertyInfo defaultComparer = comparerType.GetProperty("Default");
                _comparer = (IComparer)defaultComparer.GetValue(null, null);
            }

            public override int Compare(T x, T y)
            {
                object xValue = _property.GetValue(x);
                object yValue = _property.GetValue(y);


                if (_direction == ListSortDirection.Ascending)
                {
                    return _comparer.Compare(xValue, yValue);
                }
                else
                {
                    return _comparer.Compare(yValue, xValue);
                }
            }
        }

        protected override bool SupportsSortingCore
        {
            get { return true; }
        }

        protected override bool IsSortedCore
        {
            get { return _isSorted; }
        }

        protected override void RemoveSortCore()
        {
            _isSorted = false;
        }

        protected override void ApplySortCore(PropertyDescriptor prop, ListSortDirection direction)
        {
            if (prop.PropertyType.GetInterface("IComparable") != null)
            {
                List<T> items = this.Items as List<T>;

                if (items != null)
                {
                    PropertyComparer<T> pc = new PropertyComparer<T>(prop, direction);
                    items.Sort(pc);
                    _isSorted = true;
                }
                else
                {
                    _isSorted = false;
                }

            }
            else
            {
                throw new Exception("Property can't be compared");
            }
        }

        protected override bool SupportsSearchingCore
        {
            get { return true; }
        }

        protected override int FindCore(PropertyDescriptor prop, object key)
        {
            // Specify search columns
            if (prop == null) return -1;

            // Get list to search
            List<T> items = this.Items as List<T>;

            // Traverse list for value
            foreach (T item in items)
            {
                if (prop.GetValue(item) != null)
                {
                    // Test column search value
                    string value = prop.GetValue(item).ToString();

                    // If value is the search value, return the 
                    // index of the data item
                    if (value.Contains((string)key)) return IndexOf(item);
                }

            }
            return -1;
        }

    }
}
