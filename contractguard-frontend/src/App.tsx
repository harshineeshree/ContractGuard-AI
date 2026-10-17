import { useEffect, useState } from "react";

const API_URL = "/api";

interface Contract {
  id: string;
  filename: string;
  contract_type: string | null;
  parties: string | null;
  effective_date: string | null;
  expiration_date: string | null;
  contract_duration: string | null;
  renewal_terms: string | null;
  renewal_notice_period: string | null;
  renewal_deadline: string | null;
  renewal_deadline_status: string | null;
  termination_notice_period: string | null;
  payment_amount: string | null;
  payment_frequency: string | null;
  confidentiality: string | null;
  governing_law: string | null;
  dispute_resolution: string | null;
  scope_of_work: string | null;
  important_obligations: string | null;
  risk_level: string | null;
  status: string | null;
  created_at: string;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [contracts, setContracts] = useState<Contract[]>([]);

  // --------------------------------------------------
  // Load Contract History
  // --------------------------------------------------

  const loadContracts = async () => {
    try {
      const response = await fetch(
        `${API_URL}/contracts`
      );

      if (!response.ok) {
        throw new Error("Failed to load contracts");
      }

      const data = await response.json();

      setContracts(data.contracts || []);
    } catch (error) {
      console.error(
        "Failed to load contract history:",
        error
      );
    }
  };

  // Load contracts when page opens
  useEffect(() => {
    loadContracts();
  }, []);

  // --------------------------------------------------
  // Analyze Contract
  // --------------------------------------------------

  const analyzeContract = async () => {
    if (!file) {
      setError("Please select a contract file.");
      return;
    }

    setLoading(true);
    setReport("");
    setError("");

    const formData = new FormData();

    formData.append("file", file);

    try {
      const response = await fetch(
        `${API_URL}/contracts/analyze`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const errorText = await response.text();

        throw new Error(
          `Backend error ${response.status}: ${errorText}`
        );
      }

      const data = await response.json();

      // Display analysis report
      setReport(data.report);

      // Refresh contract history
      await loadContracts();

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // Extract values from generated report
  // --------------------------------------------------

  const getValue = (label: string) => {
    const match = report.match(
      new RegExp(
        `${label}:\\s*\\n([^\\n]+)`,
        "i"
      )
    );

    return match
      ? match[1].trim()
      : "Not specified";
  };

  const getRiskLevel = () => {
    const match = report.match(
      /Overall Risk Level:\s*\n([^\n]+)/i
    );

    return match
      ? match[1].trim()
      : "Unknown";
  };

  const riskLevel = getRiskLevel();

  // --------------------------------------------------
  // UI
  // --------------------------------------------------

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* HEADER */}

      <header className="border-b border-slate-800 bg-slate-950">

        <div className="mx-auto flex max-w-7xl items-center justify-between px-8 py-5">

          <div>

            <h1 className="text-2xl font-bold">
              🛡️ ContractGuard AI
            </h1>

            <p className="mt-1 text-sm text-slate-400">
              Contract Intelligence & Compliance Platform
            </p>

          </div>

          <div className="rounded-full border border-slate-700 px-4 py-2 text-xs text-slate-400">
            AI Contract Analysis
          </div>

        </div>

      </header>


      <main className="mx-auto max-w-7xl px-8 py-10">

        {/* PAGE TITLE */}

        <div className="mb-8">

          <h2 className="text-4xl font-bold">
            Analyze Your Contract
          </h2>

          <p className="mt-3 text-slate-400">
            Upload a PDF, DOCX, or TXT contract for automated
            intelligence and compliance analysis.
          </p>

        </div>


        {/* UPLOAD SECTION */}

        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-8">

          <div className="rounded-xl border-2 border-dashed border-slate-700 p-10 text-center">

            <div className="text-6xl">
              📄
            </div>

            <h3 className="mt-5 text-xl font-semibold">
              Upload Contract
            </h3>

            <p className="mt-2 text-sm text-slate-400">
              Supported formats: PDF, DOCX, TXT
            </p>


            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={(event) => {

                setFile(
                  event.target.files?.[0] || null
                );

                setError("");
                setReport("");

              }}
              className="mx-auto mt-6 block max-w-full text-sm text-slate-300"
            />


            {file && (

              <div className="mx-auto mt-5 max-w-md rounded-lg bg-slate-800 p-4">

                <p className="text-sm text-green-400">
                  ✓ Selected contract
                </p>

                <p className="mt-1 truncate text-sm text-white">
                  {file.name}
                </p>

              </div>

            )}


            <button
              onClick={analyzeContract}
              disabled={loading}
              className="mt-6 rounded-lg bg-blue-600 px-8 py-3 font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >

              {loading
                ? "Analyzing Contract..."
                : "Analyze Contract"}

            </button>

          </div>


          {/* ERROR */}

          {error && (

            <div className="mt-6 rounded-lg border border-red-800 bg-red-950 p-4 text-red-300">

              {error}

            </div>

          )}

        </section>


        {/* CONTRACT HISTORY */}

        <section className="mt-10">

          <div className="mb-5">

            <h2 className="text-2xl font-bold">
              Contract History
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Previously analyzed contracts stored in ContractGuard
            </p>

          </div>


          {contracts.length === 0 ? (

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center text-slate-400">

              No contracts analyzed yet.

            </div>

          ) : (

            <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">

              <div className="overflow-x-auto">

                <table className="w-full text-left">

                  <thead className="border-b border-slate-800 bg-slate-950">

                    <tr>

                      <th className="px-6 py-4 text-sm text-slate-400">
                        Contract
                      </th>

                      <th className="px-6 py-4 text-sm text-slate-400">
                        Type
                      </th>

                      <th className="px-6 py-4 text-sm text-slate-400">
                        Risk
                      </th>

                      <th className="px-6 py-4 text-sm text-slate-400">
                        Status
                      </th>

                      <th className="px-6 py-4 text-sm text-slate-400">
                        Expiration
                      </th>

                    </tr>

                  </thead>


                  <tbody>

                    {contracts.map((contract) => (

                      <tr
                        key={contract.id}
                        className="border-b border-slate-800 last:border-0 hover:bg-slate-800/50"
                      >

                        {/* CONTRACT */}

                        <td className="px-6 py-5">

                          <p className="font-medium text-white">
                            {contract.filename}
                          </p>

                          <p className="mt-1 text-xs text-slate-500">
                            Analyzed{" "}
                            {new Date(
                              contract.created_at
                            ).toLocaleString()}
                          </p>

                        </td>


                        {/* TYPE */}

                        <td className="px-6 py-5 text-sm text-slate-300">

                          {contract.contract_type ||
                            "Not specified"}

                        </td>


                        {/* RISK */}

                        <td className="px-6 py-5">

                          <span
                            className={`rounded-full px-3 py-1 text-xs font-semibold ${
                              contract.risk_level ===
                              "High"
                                ? "bg-red-950 text-red-400"
                                : contract.risk_level ===
                                  "Medium"
                                ? "bg-yellow-950 text-yellow-400"
                                : "bg-green-950 text-green-400"
                            }`}
                          >

                            {contract.risk_level ||
                              "Unknown"}

                          </span>

                        </td>


                        {/* STATUS */}

                        <td className="px-6 py-5 text-sm text-green-400">

                          {contract.status ||
                            "Unknown"}

                        </td>


                        {/* EXPIRATION */}

                        <td className="px-6 py-5 text-sm text-slate-300">

                          {contract.expiration_date ||
                            "Not specified"}

                        </td>

                      </tr>

                    ))}

                  </tbody>

                </table>

              </div>

            </div>

          )}

        </section>


        {/* ANALYSIS DASHBOARD */}

        {report && (

          <div className="mt-10">

            {/* SUMMARY CARDS */}

            <div className="grid gap-5 md:grid-cols-3">


              {/* CONTRACT TYPE */}

              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

                <p className="text-sm text-slate-400">
                  Contract Type
                </p>

                <h3 className="mt-3 text-xl font-semibold">
                  {getValue("Contract Type")}
                </h3>

              </div>


              {/* RISK */}

              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

                <p className="text-sm text-slate-400">
                  Risk Level
                </p>

                <h3
                  className={`mt-3 text-xl font-bold ${
                    riskLevel === "High"
                      ? "text-red-400"
                      : riskLevel === "Medium"
                      ? "text-yellow-400"
                      : "text-green-400"
                  }`}
                >

                  {riskLevel}

                </h3>

              </div>


              {/* STATUS */}

              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

                <p className="text-sm text-slate-400">
                  Contract Status
                </p>

                <h3 className="mt-3 text-xl font-semibold text-green-400">
                  {getValue("Contract Status")}
                </h3>

              </div>

            </div>


            {/* CONTRACT INFORMATION */}

            <section className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-8">

              <h2 className="text-2xl font-bold">
                Contract Information
              </h2>

              <div className="mt-6 grid gap-5 md:grid-cols-2">

                <InfoCard
                  title="Parties"
                  value={getValue("Parties")}
                />

                <InfoCard
                  title="Effective Date"
                  value={getValue("Effective Date")}
                />

                <InfoCard
                  title="Expiration Date"
                  value={getValue("Expiration Date")}
                />

                <InfoCard
                  title="Contract Duration"
                  value={getValue(
                    "Contract Duration"
                  )}
                />

                <InfoCard
                  title="Payment"
                  value={`${getValue(
                    "Payment"
                  )} ${getValue(
                    "Payment Frequency"
                  )}`}
                />

                <InfoCard
                  title="Termination Notice"
                  value={getValue(
                    "Termination Notice Period"
                  )}
                />

              </div>

            </section>


            {/* RENEWAL ALERT */}

            <section className="mt-6 rounded-2xl border border-yellow-900 bg-yellow-950/30 p-8">

              <div className="flex items-start gap-4">

                <div className="text-3xl">
                  ⚠️
                </div>

                <div>

                  <h2 className="text-xl font-bold text-yellow-400">
                    Renewal Alert
                  </h2>

                  <p className="mt-2 text-slate-300">
                    {getValue("Renewal Terms")}
                  </p>

                  <div className="mt-4 grid gap-4 md:grid-cols-2">

                    <div>

                      <p className="text-xs text-slate-500">
                        Renewal Deadline
                      </p>

                      <p className="mt-1 font-semibold">
                        {getValue(
                          "Renewal Deadline"
                        )}
                      </p>

                    </div>


                    <div>

                      <p className="text-xs text-slate-500">
                        Notice Period
                      </p>

                      <p className="mt-1 font-semibold">
                        {getValue(
                          "Renewal Notice Period"
                        )}
                      </p>

                    </div>

                  </div>

                </div>

              </div>

            </section>


            {/* RISK ANALYSIS */}

            <section className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-8">

              <h2 className="text-2xl font-bold">
                Risk Analysis
              </h2>

              <p className="mt-2 text-sm text-slate-400">
                Potential issues identified during automated
                contract analysis.
              </p>

              <div className="mt-6">

                <pre className="whitespace-pre-wrap text-sm leading-7 text-slate-300">
                  {report.split(
                    "RISK INFORMATION"
                  )[1] ||
                    "No risk information available."}
                </pre>

              </div>

            </section>


            {/* FULL REPORT */}

            <details className="mt-6 rounded-2xl border border-slate-800 bg-slate-900">

              <summary className="cursor-pointer px-8 py-5 font-semibold text-slate-300">
                View Complete Analysis Report
              </summary>

              <div className="border-t border-slate-800 p-8">

                <pre className="whitespace-pre-wrap text-sm leading-7 text-slate-400">
                  {report}
                </pre>

              </div>

            </details>

          </div>

        )}

      </main>


      {/* FOOTER */}

      <footer className="border-t border-slate-800 py-8 text-center text-sm text-slate-500">

        ContractGuard AI • Contract Intelligence & Compliance

      </footer>

    </div>
  );
}


// --------------------------------------------------
// Info Card Component
// --------------------------------------------------

function InfoCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div className="rounded-xl bg-slate-950 p-5">

      <p className="text-xs uppercase tracking-wide text-slate-500">
        {title}
      </p>

      <p className="mt-2 break-words text-sm leading-6 text-slate-200">
        {value}
      </p>

    </div>
  );
}


export default App;