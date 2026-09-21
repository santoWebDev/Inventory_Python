import { useEffect, useState } from "react";
import { getSalesReport } from "../../api/reportApi";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";
import Button from "../../components/Button";
import { downloadCsv } from "../../utils/downloadCsv";

const SalesReport = () => {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await getSalesReport();

      console.log("Sales Report Response:", response);

      setReport(response.data);
    } catch (e) {
      console.error("Sales Report Error:", e);

      setError(
        e.response?.data?.message || "Failed to load sales report"
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const downloadReport = () => {
    if (!report) return;

    const rows = report.orders.map((order) => ({
      Order_ID: order.id,
      Order_Number: order.order_number,
      Customer_ID: order.customer_id || "",
      Total_Amount: order.total_amount,
      Status: order.status,
      Created_At: order.created_at,
    }));

    if (rows.length === 0) {
      rows.push({
        Order_ID: "",
        Order_Number: "",
        Customer_ID: "",
        Total_Amount: "",
        Status: "No orders",
        Created_At: "",
      });
    }

    downloadCsv("sales-report.csv", rows);
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
            Sales Report
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Sales and order performance
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
          <div className="grid gap-4 md:grid-cols-2">

            {/* Total Orders */}
            <div className="rounded-xl bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Total Orders
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {report.totalOrders}
              </p>
            </div>

            {/* Total Sales */}
            <div className="rounded-xl bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Total Sales
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                ₹
                {Number(report.totalSales).toLocaleString("en-IN")}
              </p>
            </div>

          </div>

          {/* Orders Table */}
          <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">

            <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
              <div>
                <h2 className="font-semibold text-slate-900">
                  Sales Orders
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  Completed and active sales orders
                </p>
              </div>
            </div>

            <div className="w-full max-w-full overflow-x-auto">

              <table className="w-full min-w-[700px] text-sm">

                <thead className="bg-slate-50 text-left">

                  <tr>
                    <th className="px-4 py-3">
                      Order #
                    </th>

                    <th className="px-4 py-3">
                      Customer
                    </th>

                    <th className="px-4 py-3">
                      Amount
                    </th>

                    <th className="px-4 py-3">
                      Status
                    </th>

                    <th className="px-4 py-3">
                      Date
                    </th>
                  </tr>

                </thead>

                <tbody>

                  {report.orders.length === 0 ? (

                    <tr>
                      <td
                        colSpan="5"
                        className="px-4 py-12 text-center"
                      >
                        <div className="text-slate-500">
                          <p className="text-base font-medium">
                            No sales orders found
                          </p>

                          <p className="mt-1 text-sm">
                            Sales will appear here when orders are created.
                          </p>
                        </div>
                      </td>
                    </tr>

                  ) : (

                    report.orders.map((order) => (

                      <tr
                        key={order.id}
                        className="border-t border-slate-100 transition hover:bg-slate-50/70"
                      >

                        <td className="px-4 py-3 font-semibold">
                          {order.order_number}
                        </td>

                        <td className="px-4 py-3">
                          {order.customer_id || "-"}
                        </td>

                        <td className="px-4 py-3">
                          ₹
                          {Number(
                            order.total_amount
                          ).toLocaleString("en-IN")}
                        </td>

                        <td className="px-4 py-3">
                          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium capitalize">
                            {order.status}
                          </span>
                        </td>

                        <td className="px-4 py-3">
                          {order.created_at
                            ? new Date(
                                order.created_at
                              ).toLocaleDateString("en-IN")
                            : "-"}
                        </td>

                      </tr>

                    ))

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

export default SalesReport;