export default function PageHeader({ eyebrow = "SENTINELTRADE", title, description, action }) {
  return (
    <div className="page-header">
      <div>
        <span className="page-eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
        {description && <p>{description}</p>}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}
