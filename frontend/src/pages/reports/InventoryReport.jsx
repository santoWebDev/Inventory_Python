import { useEffect, useState } from "react";
import { getInventoryReport } from "../../api/reportApi";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";
import Button from "../../components/Button";
import { downloadCsv } from "../../utils/downloadCsv";

const InventoryReport = () => {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await getInventoryReport();

      console.log("Inventory Report Response:", response);

      setReport(response.data);
    } catch (e) {
      console.error("Inventory Report Error:", e);

      setError(
        e.response?.data?.message ||
          "Failed to load inventory report"
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const getStockStatus = (product) => {
    if (product.stock === 0) {
      return "Out of Stock";
    }

    if (product.stock <= product.low_stock_threshold) {
      return "Low Stock";
    }

    return "In Stock";
  };

  const downloadReport = () => {
    if (!report) return;

    const rows = report.products.map((product) => ({
      Product_ID: product.id,
      Product: product.name,
      Price: product.price,
      Stock: product.stock,
      Low_Stock_Threshold: product.low_stock_threshold,
      Stock_Status: getStockStatus(product),
      Status: product.status,
    }));

    if (rows.length === 0) {
      rows.push({
        Product_ID: "",
        Product: "No products",
        Price: "",
        Stock: "",
        Low_Stock_Threshold: "",
        Stock_Status: "",
        Status: "",
      });
    }

    downloadCsv("inventory-report.csv", rows);
  };

  return (
    <div className="w-full min-w-0 space-y-5 sm:space-y-6">

      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.18em] text-indigo-500">
            Analytics
          </p>

          <h1 className="mt-1 text-2xl font-bold text-slate-900">
            Inventory Report
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Current stock and inventory overview
          </p>
        </div>

        <Button
          variant="secondary"
          onClick={downloadReport}
          disabled={!report}
        >
          ↓ Download CSV
        </Button>
      </div>

      {/* Error */}
      <ErrorMessage message={error} />

      {/* Loading */}
      {loading ? (
        <Loader />
      ) : report ? (
        <>
          {/* Summary Cards */}
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

            {/* Total Products */}
            <div className="rounded-xl bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Total Products
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {report.totalProducts}
              </p>
            </div>

            {/* Total Stock */}
            <div className="rounded-xl bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Total Stock
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {report.totalStock}
              </p>
            </div>

            {/* Low Stock */}
            <div className="rounded-xl bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Low Stock
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {report.lowStock}
              </p>
            </div>

            {/* Out of Stock */}
            <div className="rounded-xl bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Out of Stock
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {report.outOfStock}
              </p>
            </div>

          </div>

          {/* Products Table */}
          <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">

            <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
              <div>
                <h2 className="font-semibold text-slate-900">
                  Inventory
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  Current stock levels for all products
                </p>
              </div>
            </div>

            <div className="w-full max-w-full overflow-x-auto">

              <table className="w-full min-w-[800px] text-sm">

                <thead className="bg-slate-50 text-left">

                  <tr>
                    <th className="px-4 py-3">
                      Product
                    </th>

                    <th className="px-4 py-3">
                      Price
                    </th>

                    <th className="px-4 py-3">
                      Stock
                    </th>

                    <th className="px-4 py-3">
                      Threshold
                    </th>

                    <th className="px-4 py-3">
                      Stock Status
                    </th>

                    <th className="px-4 py-3">
                      Status
                    </th>
                  </tr>

                </thead>

                <tbody>

                  {report.products.length === 0 ? (

                    <tr>
                      <td
                        colSpan="6"
                        className="px-4 py-12 text-center"
                      >
                        <div className="text-slate-500">
                          <p className="text-base font-medium">
                            No products found
                          </p>

                          <p className="mt-1 text-sm">
                            Products will appear here after they are added.
                          </p>
                        </div>
                      </td>
                    </tr>

                  ) : (

                    report.products.map((product) => {

                      const stockStatus =
                        getStockStatus(product);

                      return (
                        <tr
                          key={product.id}
                          className="border-t border-slate-100 transition hover:bg-slate-50/70"
                        >

                          <td className="px-4 py-3 font-semibold">
                            {product.name}
                          </td>

                          <td className="px-4 py-3">
                            ₹
                            {Number(
                              product.price
                            ).toLocaleString("en-IN")}
                          </td>

                          <td className="px-4 py-3 font-medium">
                            {product.stock}
                          </td>

                          <td className="px-4 py-3">
                            {product.low_stock_threshold}
                          </td>

                          <td className="px-4 py-3">

                            <span
                              className={`rounded-full px-3 py-1 text-xs font-medium ${
                                stockStatus === "Out of Stock"
                                  ? "bg-red-100 text-red-700"
                                  : stockStatus === "Low Stock"
                                  ? "bg-amber-100 text-amber-700"
                                  : "bg-emerald-100 text-emerald-700"
                              }`}
                            >
                              {stockStatus}
                            </span>

                          </td>

                          <td className="px-4 py-3">

                            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium capitalize">
                              {product.status}
                            </span>

                          </td>

                        </tr>
                      );
                    })

                  )}

                </tbody>

              </table>

            </div>

          </div>
        </>
      ) : null}

    </div>
  );
};

export default InventoryReport;   