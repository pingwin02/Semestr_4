namespace Lab1
{
    public static class Extensions
    {
        public static DateTime GetOldestDate(this DirectoryInfo directory)
        {
            DateTime oldestDate = DateTime.Now;

            foreach (FileInfo file in directory.GetFiles())
            {
                if (file.CreationTime < oldestDate)
                {
                    oldestDate = file.CreationTime;
                }
            }

            foreach (DirectoryInfo dir in directory.GetDirectories())
            {
                DateTime time = GetOldestDate(dir);
                if (time < oldestDate)
                {
                    oldestDate = time;
                }
            }

            return oldestDate;
        }

        public static string GetRahs(this FileSystemInfo fsi)
        {
            string rahs = "";

            FileAttributes attributes = fsi.Attributes;

            if ((FileAttributes.ReadOnly & attributes) == FileAttributes.ReadOnly)
            {
                rahs += 'r';
            }
            else
            {
                rahs += '-';
            }
            if ((FileAttributes.Archive & attributes) == FileAttributes.Archive)
            {
                rahs += 'a';
            }
            else
            {
                rahs += '-';
            }
            if ((FileAttributes.Hidden & attributes) == FileAttributes.Hidden)
            {
                rahs += 'h';
            }
            else
            {
                rahs += '-';
            }
            if ((FileAttributes.System & attributes) == FileAttributes.System)
            {
                rahs += 's';
            }
            else
            {
                rahs += '-';
            }

            return rahs;
        }
    }
}
