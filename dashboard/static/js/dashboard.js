const state = {
    data: null
};


async function api(url, options = {}) {

    const response = await fetch(
        url,
        options
    );

    if (!response.ok) {

        throw new Error(
            `API error: ${response.status}`
        );
    }

    return response.json();
}


/* ============================================================
   HELPERS
   ============================================================ */

function escapeHtml(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function formatMoney(value) {

    const number = Number(value || 0);

    return "$" + number.toFixed(2);
}


function formatDate(value) {

    if (!value) {
        return "—";
    }

    try {

        return new Date(value)
            .toLocaleString();

    } catch {

        return value;
    }
}


function stateBadge(state) {

    const value =
        String(state || "")
            .toLowerCase();

    if (value === "running") {

        return `
            <span class="badge badge-green">
                RUNNING
            </span>
        `;
    }

    if (value === "stopped") {

        return `
            <span class="badge badge-yellow">
                STOPPED
            </span>
        `;
    }

    return `
        <span class="badge badge-blue">
            ${escapeHtml(
                String(state || "UNKNOWN")
            )}
        </span>
    `;
}


function riskBadge(risk) {

    const value =
        String(risk || "UNKNOWN")
            .toUpperCase();

    let css = "badge-blue";

    if (value === "LOW") {
        css = "badge-green";
    }

    if (value === "MEDIUM") {
        css = "badge-yellow";
    }

    if (
        value === "HIGH" ||
        value === "CRITICAL"
    ) {
        css = "badge-red";
    }

    return `
        <span class="badge ${css}">
            ${escapeHtml(value)}
        </span>
    `;
}


function decisionBadge(decision) {

    const value =
        String(decision || "UNKNOWN")
            .toUpperCase();

    let css = "badge-blue";

    if (
        value === "DO_NOTHING" ||
        value === "APPROVED"
    ) {
        css = "badge-green";
    }

    if (
        value === "REVIEW" ||
        value === "REVIEW_REQUIRED"
    ) {
        css = "badge-yellow";
    }

    if (
        value === "REJECTED" ||
        value === "BLOCKED"
    ) {
        css = "badge-red";
    }

    return `
        <span class="badge ${css}">
            ${escapeHtml(value)}
        </span>
    `;
}


/* ============================================================
   DASHBOARD
   ============================================================ */

async function loadDashboard() {

    try {

        const data =
            await api(
                "/api/dashboard"
            );

        state.data = data;

        renderSummary(
            data.summary
        );

        renderResources(
            data.resources,
            data.metrics,
            data.resource_costs,
            data.audits
        );

        renderRecommendations(
            data.audits
        );

        renderAI(
            data.audits
        );

        renderAudit(
            data.audits
        );

        document.getElementById(
            "lastUpdated"
        ).textContent =
            "Updated " +
            new Date().toLocaleTimeString();

    } catch (error) {

        console.error(error);

        showToast(
            "Could not load dashboard data."
        );
    }
}


/* ============================================================
   SUMMARY
   ============================================================ */

function renderSummary(summary) {

    document.getElementById(
        "resourceCount"
    ).textContent =
        summary.resources;

    document.getElementById(
        "resourceMeta"
    ).textContent =
        `${summary.running} running · ${summary.stopped} stopped`;

    document.getElementById(
        "savings"
    ).textContent =
        formatMoney(
            summary.potential_savings
        );

    document.getElementById(
        "reviewCount"
    ).textContent =
        summary.review_required;

    document.getElementById(
        "llmSuccess"
    ).textContent =
        `${summary.llm_success_rate}%`;
}


/* ============================================================
   RESOURCE TABLE
   ============================================================ */

function renderResources(
    resources,
    metrics,
    costs,
    audits
) {

    const table =
        document.getElementById(
            "resourceTable"
        );

    const metricMap =
        new Map(
            metrics.map(
                item => [
                    String(item.resource_id),
                    item
                ]
            )
        );

    const costMap =
        new Map(
            costs.map(
                item => [
                    String(item.resource_id),
                    item
                ]
            )
        );


    const auditMap =
        new Map();

    audits.forEach(
        audit => {

            if (
                audit.resource_id !== null &&
                audit.resource_id !== undefined
            ) {

                const key =
                    String(
                        audit.resource_id
                    );

                if (!auditMap.has(key)) {
                    auditMap.set(
                        key,
                        audit
                    );
                }
            }
        }
    );


    if (!resources.length) {

        table.innerHTML = `
            <tr>
                <td colspan="9">
                    No resources found.
                </td>
            </tr>
        `;

        return;
    }


    table.innerHTML =
        resources.map(
            resource => {

                const metric =
                    metricMap.get(
                        String(resource.id)
                    );

                const cost =
                    costMap.get(
                        String(resource.id)
                    );

                const audit =
                    auditMap.get(
                        String(resource.id)
                    );


                const cpu =
                    metric &&
                    metric.cpu_average !== null
                        ? `${Number(
                            metric.cpu_average
                        ).toFixed(2)}%`
                        : "NO DATA";


                const resourceCost =
                    cost
                        ? formatMoney(
                            cost.total_cost
                        )
                        : "Not attributed";


                return `

                    <tr>

                        <td>
                            <span class="resource-id">
                                ${escapeHtml(
                                    resource.resource_id
                                )}
                            </span>

                            <div class="rec-resource">
                                ${escapeHtml(
                                    resource.name || ""
                                )}
                            </div>
                        </td>

                        <td>
                            ${escapeHtml(
                                resource.instance_type ||
                                resource.resource_type ||
                                "—"
                            )}
                        </td>

                        <td>
                            ${escapeHtml(
                                resource.region
                            )}
                        </td>

                        <td>
                            ${stateBadge(
                                resource.state
                            )}
                        </td>

                        <td>
                            ${cpu}
                        </td>

                        <td>
                            ${resourceCost}
                        </td>

                        <td>
                            ${
                                audit
                                    ? escapeHtml(
                                        audit.recommendation ||
                                        "NONE"
                                    )
                                    : "NONE"
                            }
                        </td>

                        <td>
                            ${
                                audit
                                    ? riskBadge(
                                        audit.risk_level
                                    )
                                    : riskBadge(
                                        "LOW"
                                    )
                            }
                        </td>

                        <td>
                            ${
                                audit
                                    ? decisionBadge(
                                        audit.decision
                                    )
                                    : decisionBadge(
                                        "DO_NOTHING"
                                    )
                            }
                        </td>

                    </tr>

                `;

            }
        ).join("");
}


/* ============================================================
   RECOMMENDATIONS
   ============================================================ */

function renderRecommendations(
    audits
) {

    const container =
        document.getElementById(
            "recommendationList"
        );


    if (!audits.length) {

        container.innerHTML = `
            <div class="recommendation">
                No recommendations available.
            </div>
        `;

        return;
    }


    container.innerHTML =
        audits.slice(0, 10)
            .map(
                audit => `

                    <div class="recommendation">

                        <div class="rec-top">

                            <div>

                                <div class="rec-name">
                                    ${escapeHtml(
                                        audit.recommendation ||
                                        "NO_RECOMMENDATION"
                                    )}
                                </div>

                                <div class="rec-resource">
                                    Resource:
                                    ${escapeHtml(
                                        audit.resource_id ??
                                        "N/A"
                                    )}
                                </div>

                            </div>

                            ${
                                decisionBadge(
                                    audit.decision
                                )
                            }

                        </div>


                        <div class="rec-bottom">

                            ${riskBadge(
                                audit.risk_level
                            )}

                            <span class="badge badge-blue">
                                ${
                                    audit.priority ||
                                    "LOW"
                                }
                            </span>

                            <span class="badge badge-purple">
                                Savings:
                                ${formatMoney(
                                    audit.estimated_savings
                                )}
                            </span>

                        </div>

                    </div>

                `
            ).join("");
}


/* ============================================================
   AI
   ============================================================ */

function renderAI(audits) {

    const container =
        document.getElementById(
            "aiInsight"
        );


    const completed =
        audits.filter(
            audit =>
                audit.llm_status ===
                "COMPLETED"
        );


    if (!completed.length) {

        container.textContent =
            "No completed LLM recommendations available.";

        return;
    }


    const audit =
        completed[0];


    container.innerHTML = `

        <div class="ai-resource">

            Resource:
            ${escapeHtml(
                audit.resource_id
            )}

        </div>

        <strong>
            ${escapeHtml(
                audit.llm_model ||
                "Ollama"
            )}
        </strong>

        <br><br>

        ${
            escapeHtml(
                audit.llm_recommendation ||
                "No AI recommendation available."
            )
        }

    `;
}


/* ============================================================
   AUDIT
   ============================================================ */

function renderAudit(audits) {

    const container =
        document.getElementById(
            "auditTimeline"
        );


    if (!audits.length) {

        container.innerHTML = `
            <div class="audit-item">
                No audit records found.
            </div>
        `;

        return;
    }


    container.innerHTML =
        audits.slice(0, 12)
            .map(
                audit => `

                    <div class="audit-item">

                        <div class="audit-title">

                            ${
                                escapeHtml(
                                    audit.event_type ||
                                    "ANALYSIS"
                                )
                            }

                            ·

                            ${
                                escapeHtml(
                                    audit.recommendation ||
                                    "NO_RECOMMENDATION"
                                )
                            }

                        </div>


                        <div class="audit-meta">

                            Resource:
                            ${
                                escapeHtml(
                                    audit.resource_id ??
                                    "N/A"
                                )
                            }

                            ·

                            ${
                                formatDate(
                                    audit.created_at
                                )
                            }

                        </div>


                        <div class="audit-decision">

                            ${
                                riskBadge(
                                    audit.risk_level
                                )
                            }

                            ${
                                decisionBadge(
                                    audit.decision
                                )
                            }

                            ${
                                audit.execution_status
                                    ? `
                                        <span class="badge badge-blue">
                                            ${escapeHtml(
                                                audit.execution_status
                                            )}
                                        </span>
                                      `
                                    : ""
                            }

                        </div>

                    </div>

                `
            ).join("");
}


/* ============================================================
   HEALTH
   ============================================================ */

async function loadHealth() {

    const dot =
        document.getElementById(
            "systemDot"
        );

    const status =
        document.getElementById(
            "systemStatus"
        );


    try {

        const data =
            await api(
                "/api/health"
            );


        if (
            data.database &&
            data.ollama
        ) {

            dot.className =
                "status-dot online";

            status.textContent =
                "Database + Ollama online";

        } else {

            dot.className =
                "status-dot";

            status.textContent =
                "System partially available";
        }

    } catch {

        dot.className =
            "status-dot offline";

        status.textContent =
            "Backend unavailable";
    }
}


/* ============================================================
   RUN ANALYSIS
   ============================================================ */

async function runAnalysis() {

    const button =
        document.getElementById(
            "runAnalysis"
        );

    const status =
        document.getElementById(
            "analysisStatus"
        );


    button.disabled = true;

    button.innerHTML =
        "⟳ Running Analysis...";


    status.textContent =
        "🔄 Running cloud analysis...";


    showToast(
        "🔄 Running cloud analysis..."
    );


    try {

        status.textContent =
            "Fetching AWS resources → analyzing metrics → generating recommendations → updating dashboard";


        const result =
            await api(
                "/api/run-analysis",
                {
                    method: "POST"
                }
            );


        if (
            result.success === true &&
            result.status === "COMPLETED"
        ) {

            status.textContent =
                `✅ Analysis completed successfully. ` +
                `${result.resources_analyzed || 0} resources analyzed.`;


            showToast(
                "✅ Analysis completed successfully."
            );


            await loadDashboard();

        } else {

            throw new Error(
                result.error ||
                result.message ||
                "Analysis failed."
            );
        }


    } catch (error) {

        console.error(
            "Analysis error:",
            error
        );


        status.textContent =
            "❌ Analysis failed. Check the Flask terminal for details.";


        showToast(
            "❌ Analysis failed: " +
            error.message
        );


    } finally {

        button.disabled = false;

        button.innerHTML =
            "<span>▶</span> Run Analysis";
    }
}


/* ============================================================
REFRESH DASHBOARD
============================================================ */

async function refreshDashboard() {

    const button =
        document.getElementById(
            "refreshDashboard"
        );

    const status =
        document.getElementById(
            "analysisStatus"
        );


    button.disabled = true;

    button.innerHTML =
        "⟳ Refreshing...";


    try {

        await loadDashboard();

        status.textContent =
            "Dashboard refreshed from PostgreSQL.";

        showToast(
            "↻ Dashboard refreshed."
        );

    } catch (error) {

        console.error(
            "Refresh error:",
            error
        );

        status.textContent =
            "❌ Could not refresh dashboard.";

        showToast(
            "❌ Dashboard refresh failed."
        );

    } finally {

        button.disabled = false;

        button.innerHTML =
            "↻ Refresh Dashboard";
    }
}

/* ============================================================
   TOAST
   ============================================================ */

let toastTimer = null;


function showToast(message) {

    const toast =
        document.getElementById(
            "toast"
        );

    toast.textContent =
        message;

    toast.classList.add(
        "show"
    );


    clearTimeout(
        toastTimer
    );


    toastTimer =
        setTimeout(
            () => {

                toast.classList.remove(
                    "show"
                );

            },
            3000
        );
}


/* ============================================================
   INIT
   ============================================================ */

document.addEventListener(
"DOMContentLoaded",
() => {

    document.getElementById(
        "runAnalysis"
    ).addEventListener(
        "click",
        runAnalysis
    );


    document.getElementById(
        "refreshDashboard"
    ).addEventListener(
        "click",
        refreshDashboard
    );


    loadDashboard();

    loadHealth();


    setInterval(
        loadDashboard,
        30000
    );


    setInterval(
        loadHealth,
        15000
    );

}
);
