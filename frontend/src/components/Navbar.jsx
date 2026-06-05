import React from 'react';
import { Link } from 'react-router-dom';
import { Building2, Search, User } from 'lucide-react';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar glass">
      <div className="container navbar-content">
        <Link to="/" className="brand">
          <Building2 className="brand-icon" />
          <span className="brand-text">Estate<span className="gradient-text">Node</span></span>
        </Link>
        
        <div className="nav-links">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/properties" className="nav-link">Properties</Link>
          <Link to="/agents" className="nav-link">Agents</Link>
        </div>

        <div className="nav-actions">
          <button className="icon-btn" aria-label="Search">
            <Search size={20} />
          </button>
          <Link to="/login" className="btn btn-primary btn-sm">
            <User size={18} /> Sign In
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
